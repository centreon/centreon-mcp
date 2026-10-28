# CLAUDE.md

Guidance for working in this repository.

## Project

MCP server exposing a Centreon instance's monitoring and configuration APIs as MCP tools.
Python 3.14 (`>=3.13` supported), [FastMCP](https://gofastmcp.com), `httpx`, Pydantic. Managed with `uv`.

Runs as an HTTP MCP server (`transport="http"`), not stdio.

Tracked in the `MON` Jira project — reference tickets as `MON-<id>` in branches, commits and PRs.
The work is attached to epic `MON-197998` — *MCP Server for basic configuration*.

## Commands

```shell
uv sync --dev                                              # install deps
uv run centreon-mcp-server                                 # start the server
uv run ruff check .                                        # lint (CI gate)
uv run ruff format .                                       # format (line-length 100, not CI-gated)
uv run mypy centreon_mcp                                   # type check (clean; keep it that way)
uv run pytest tests -q                                     # tests
uv run coverage run --source centreon_mcp -m pytest tests && uv run coverage report
```

Configuration comes from the environment (or `.env`, loaded via `python-dotenv`); see the README
table for the full set. `CENTREON_AUTH_PLUGIN` selects the authentication plugin (default `none`),
and the Centreon connection settings belong to that plugin: the `none` plugin requires
`CENTREON_BASE_URL` and refuses to start without it. The `FastMCP` app is built at import time as
the module-level `mcp` in `centreon_mcp/__main__.py` (it must exist for `@mcp.custom_route`, which
registers the unauthenticated `GET /health` liveness probe; it never contacts Centreon). `main()`
then loads the plugin, attaches its provider with `mcp.auth = auth.plugin.provider()` — FastMCP only
reads it when `run()` builds the HTTP app — mounts the built-in components plus
`auth.plugin.components()`, and runs. `lifespan` calls `platform/versions` on every tenant returned
by `plugin.tenants()` to prove connectivity.

## Architecture

Three layers, and almost every change touches them in this order:

1. **`centreon_mcp/types/`** — one module per Centreon entity. Each declares a Pydantic model of the
   entity plus its `*Filter`, `*Order` and `*Params` companions, and composes the CRUD mixins it
   supports. This is where all Centreon API knowledge lives (endpoint paths, field names, quirks).
2. **`centreon_mcp/utils/mixins.py`** — generic, reusable HTTP behaviour: `CreateMixin`, `ReadMixin`,
   `ListMixin`, `UpdateMixin` (via `PutMixin`/`PatchMixin`), `DeleteMixin`, `SetMixin`, `CountMixin`.
   A model gets an operation by inheriting the mixin, parameterised with its own types. Endpoints
   come from the model's `endpoint`/`set_endpoint` class vars.
3. **`centreon_mcp/components/`** — the MCP components, split by kind into two `FastMCP` sub-apps
   listed in `components/__init__.py` and mounted by `__main__.py`:
   - `components/tools/` — the MCP tools. `tools/__init__.py` builds the `tools` app and mounts one
     `FastMCP` sub-app per domain module (`configuration`, `monitoring`, `timeline`, `metric`).
     Every tool declares `auth=require_roles(Role.<LEVEL>)` — a convention nothing enforces, and a
     tool without it is open to every caller.
   - `components/prompts/` — the MCP prompts. `prompts/__init__.py` builds the `prompts` app and
     mounts one `FastMCP` sub-app per module. `diagnosis` holds `host_diagnosis(host_name)`
     (`READER`), which returns a step-by-step plan that chains the read-only tools (`list_*`, `get_*`,
     `count_*`) into a "Describe, Understand, Act" diagnosis of a host. Prompts declare
     `require_roles` like tools do. Their text names tools, `model_type` values and filter fields,
     so renaming any of them means updating the prompt too.

   A new domain module goes in the matching sub-package and is mounted from its `__init__.py`, not
   from `components/__init__.py`.

`centreon_mcp/utils/request.py` is the single exit point to the Centreon API: resolves the
`Tenant` (passed explicitly, else `auth.plugin.tenant()` for the current request), builds
`{tenant.base_url}/api/latest/{endpoint}`, sends `tenant.token` as `X-AUTH-TOKEN`, logs a
token-masked trace, and raises `CentreonAPIError` on non-2xx. It does not read request headers:
choosing the token, including honouring a client-supplied `centreon-api-token` header, is the
plugin's job in `tenant()`. The shared `AsyncClient` has no `base_url`; every request uses an
absolute URL.

### Pluggable authentication

`centreon_mcp/auth/` decides who may call which tool and which Centreon each request targets.

- Plugins subclass `AuthPlugin` (`auth/plugins/base.py`) and implement `provider()` (the FastMCP
  `AuthProvider`, or `None` for an unauthenticated server), `tenant()` (the `Tenant` — name,
  `base_url`, `api_token` — for the current request), `tenants()` (tenants known upfront, for the
  startup check) and `role(token)` (the user's `Role`). `tenants()` runs outside any HTTP request,
  where `get_http_headers()` returns `{}`.
- `role()` raises `AuthenticationError` (`auth/models.py`) to refuse an identity on purpose:
  `require_roles` denies the tool and logs one INFO line. Any other exception is a fault — FastMCP
  logs it as a warning with traceback and denies too. Never raise `AuthenticationError` for plugin
  misconfiguration, or the fault is logged as a routine refusal.
- `components()` is optional (default `[]`): `FastMCP` sub-apps the plugin mounts next to the
  built-in ones, for deployment-specific tools. They must declare `require_roles` themselves.
- Plugins are discovered through the `centreon_mcp.auth` entry-point group declared in
  `pyproject.toml`; `auth.load()` instantiates the one named by `CENTREON_AUTH_PLUGIN` into the
  module-level `auth.plugin`. A new plugin needs an entry-point line — and `uv sync` to register it.
- Each plugin owns its settings (own `BaseSettings` class, `CENTREON_` prefix); connection settings
  are no longer in the core `Settings`. `NoAuthPlugin` (`none`) serves a single Centreon from
  `CENTREON_BASE_URL`/`CENTREON_API_TOKEN` and grants `Role.ADMIN` to everyone; its `tenant()`
  prefers the `centreon-api-token` request header over `CENTREON_API_TOKEN`.
- `Role` is an ordered `IntEnum` (`NONE < READER < EDITOR < ADMIN`); `require_roles(level)` grants a
  tool when `role >= level`. Convention: `READER` for list/get/count tools, `EDITOR` for
  create/update and setting/cancelling monitoring actions, `ADMIN` for deletes and poller
  generate/reload.

### The discriminated-union tool pattern

Tools are deliberately few and wide rather than one-per-entity. `list_configurations`,
`create_configuration`, `set_monitoring_actions`, etc. take a `model_type: Literal[...]` plus a
`filters`/`params`/`order` argument typed as an `Annotated[A | B | C, Field(discriminator="model_type")]`
union (assembled in `types/configuration/__init__.py` and `types/monitoring/__init__.py`).

Two consequences to respect:

- `model_type` is duplicated: it discriminates the union **and** keys the
  `MODELS_MIXIN_{LIST,CREATE,UPDATE,DELETE,SET,COUNT}` dicts in the `mapping.py` modules, which is
  how a tool resolves the model class to call.
- Because Pydantic only validates that the payload is *one of* the union members, the tool must
  cross-check it against the selected `model_type`. Every tool calls `.check(model_type)` on its
  params/filters/order (`BaseParams.check` and friends in `utils/base.py`) before dispatching. Skip
  it and a caller can pass `host` filters to a `service_group` list.

Filters serialise into Centreon's `search` query syntax via `serialization_alias` strings of the form
`"<field> <operator>"` (e.g. `serialization_alias="name $eq"`); `BaseFilter.conditions` splits them
back apart and `BaseFilter.join` ORs multiple filters together.

`PutMixin.update` implements partial update on a PUT-only API: it GETs the current entity, merges the
partial params over it, and PUTs the result — hence the `full_params_cls` class var. Use
`PatchMixin` where the API genuinely supports PATCH.

Bulk operations (`delete`, poller generate/reload) fan out with `asyncio.gather(..., return_exceptions=True)`
and return `dict[int, bool | BaseException]` — they never raise for an individual failure.

## Adding support for a new entity

The repeated shape of most recent commits. Using `types/configuration/host_category.py` as the
reference:

1. New module in `types/configuration/` (or `types/monitoring/`) with a `DESCRIPTION` dict of field
   docs, then `<Entity>Order`, `<Entity>Filter`, `<Entity>BaseParams` →
   `<Entity>PartialParams`/`<Entity>FullParams`, and the model class inheriting `BaseModel` plus its
   mixins with `endpoint`, `model_type` and `full_params_cls` class vars.
2. Export the new names from the package `__init__.py` and add them to the relevant
   `Configuration*`/`Monitoring*` unions.
3. Register the model in the applicable `MODELS_MIXIN_*` lists in `mapping.py`.
4. Add the `model_type` literal to each tool in `components/tools/` that should accept it — the `Literal`
   lists differ per tool (e.g. `monitoring_server` is listable but not creatable). A brand-new tool
   must also declare `auth=require_roles(Role.<LEVEL>)` following the role convention above.
5. Extend the `@pytest.mark.parametrize` tables in `tests/utils/mixins/test_*.py` and the tool tests
   in `tests/components/tools/`; update `TOOLS.md` (or `PROMPTS.md` for prompts) and the README feature list if tool surface or capabilities changed.

`DESCRIPTION` dict entries are the descriptions the LLM client sees — they are the tool's real
documentation, so write them for a model that has never seen Centreon (see `time_period.py` for
format-heavy fields).

## Testing conventions

- `asyncio_mode = "auto"` — async tests need no marker.
- `tests/conftest.py` stuffs fake credentials into `os.environ` at import time; do not rely on a real
  `.env` in tests.
- Mixin tests are shared abstract bases in `tests/utils/mixins/base.py` (`__test__ = False`),
  subclassed per domain with `__test__ = True` and a `@pytest.mark.parametrize` table supplying
  `model`/`endpoint`/`params`. Adding an entity means adding rows, not new test logic.
- Everything is mocked at `centreon_mcp.utils.mixins.request` or at the component's model method —
  no test hits the network. Component tests also patch the module `logger`.
- Code that reaches `auth.plugin` (e.g. `utils/request.py`) is tested by patching the module's
  `auth` import (`patch("centreon_mcp.utils.request.auth")`) and stubbing `plugin.tenant` with an
  `AsyncMock` returning a `Tenant`; plugins themselves are tested under `tests/auth/`.
- Coverage sits at ~99%; CI runs `coverage report` after the suite.

## Conventions

- Conventional Commits with a component scope: `feat(configuration):`, `feat(monitoring):`,
  `refactor(monitoring):`, `docs:`, `chore(deps):`, `build(deps):`.
- Main branch is `develop`; PRs target it. CI runs ruff + pytest/coverage, dependency analysis, and
  gitleaks; GitHub Actions must be SHA-pinned.
- `.githooks/` holds pre-commit/pre-push dispatchers that run `gitleaks`. Never bypass them.
- File naming in `types/` is mostly snake_case (`host_group.py`) with one legacy exception
  (`monitoring/servicegroup.py`) — follow snake_case for new modules.
