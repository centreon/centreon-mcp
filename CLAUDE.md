# CLAUDE.md

Guidance for working in this repository.

## Project

MCP server exposing a Centreon instance's monitoring and configuration APIs as MCP tools.
Python 3.14 (`>=3.13` supported), [FastMCP](https://gofastmcp.com), `httpx`, Pydantic. Managed with `uv`.

Runs as an HTTP MCP server (`transport="http"`), not stdio.

Tracked in the `MON` Jira project — reference tickets as `MON-<id>` in branches, commits and PRs.
The work is attached to epic `MON-197998` — _MCP Server for basic configuration_.

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

Requires `CENTREON_BASE_URL` in the environment (or `.env`, loaded via `python-dotenv`); see the
README table for the full set. The server refuses to start without it — `lifespan` in
`centreon_mcp/server.py` calls `platform/versions` to prove connectivity before mounting components.

## Architecture

Three layers, and almost every change touches them in this order:

1. **`centreon_mcp/types/`** — one module per Centreon entity. Each declares a Pydantic model of the
   entity plus its `*Filter`, `*Order` and `*Params` companions, and composes the CRUD mixins it
   supports. This is where all Centreon API knowledge lives (endpoint paths, field names, quirks).
2. **`centreon_mcp/utils/mixins.py`** — generic, reusable HTTP behaviour: `CreateMixin`, `ReadMixin`,
   `ListMixin`, `UpdateMixin` (via `PutMixin`/`PatchMixin`), `DeleteMixin`, `SetMixin`, `CountMixin`.
   A model gets an operation by inheriting the mixin, parameterised with its own types. Endpoints
   come from the model's `endpoint`/`set_endpoint` class vars.
3. **`centreon_mcp/components/`** — the MCP tools. Five `FastMCP` sub-apps (`monitoring`, `metric`,
   `timeline`, `configuration`, `account`) listed in `components/__init__.py` and mounted by
   `server.py`.

`centreon_mcp/utils/request.py` is the single exit point to the Centreon API: asks the
authentication plugin which `Tenant` to call, builds `{tenant.base_url}/api/latest/{endpoint}`
with the tenant token, logs a token-masked trace, and raises `CentreonAPIError` on non-2xx.

### Authentication, tenants and roles

`centreon_mcp/auth/` decides who the caller is, which Centreon it reaches and what it may do. The
`AuthPlugin` protocol (`auth/base.py`) is implemented by `auth/none.py` (unauthenticated, one
Centreon, every tool granted) and `auth/oidc.py` (any OpenID Connect provider, roles and tenant read
from token claims); `CENTREON_AUTH_PLUGIN` selects one, and a deployment whose identity model fits
neither ships its own plugin in a separate package. Keep provider-specific settings inside the
plugin, never in the core `Settings`.

A plugin may also contribute its own `FastMCP` sub-apps through `components()`, mounted by the
lifespan alongside the built-in ones. That is how deployment-specific choices stay out of the
generic tools.

Permission levels are `Role.READER < Role.EDITOR < Role.ADMIN`. **Every tool declares one** through
`auth=READER | EDITOR | ADMIN` in its decorator: tools above the caller level are hidden from
`tools/list` and cannot be called. A tool shipped without `auth=` would be reachable by anyone, so
`tests/components/test_component_authorization.py` asserts the full table and fails when a tool is
added without a level. Update that table and `TOOLS.md` together. That guarantee stops at the
package boundary: tools a plugin contributes through `components()` are its own responsibility.

### The discriminated-union tool pattern

Tools are deliberately few and wide rather than one-per-entity. `list_configurations`,
`create_configuration`, `set_monitoring_actions`, etc. take a `model_type: Literal[...]` plus a
`filters`/`params`/`order` argument typed as an `Annotated[A | B | C, Field(discriminator="model_type")]`
union (assembled in `types/configuration/__init__.py` and `types/monitoring/__init__.py`).

Two consequences to respect:

- `model_type` is duplicated: it discriminates the union **and** keys the
  `MODELS_MIXIN_{LIST,CREATE,UPDATE,DELETE,SET,COUNT}` dicts in the `mapping.py` modules, which is
  how a tool resolves the model class to call.
- Because Pydantic only validates that the payload is _one of_ the union members, the tool must
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
4. Add the `model_type` literal to each tool in the component that should accept it — the `Literal`
   lists differ per tool (e.g. `monitoring_server` is listable but not creatable). A brand new tool
   also needs its `auth=` level and a row in the authorization test table.
5. Extend the `@pytest.mark.parametrize` tables in `tests/utils/mixins/test_*.py` and the component
   tests; update `TOOLS.md` and the README feature list if tool surface or capabilities changed.

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
- Coverage sits at ~99%; CI runs `coverage report` after the suite.

## Conventions

- Conventional Commits with a component scope: `feat(configuration):`, `feat(monitoring):`,
  `refactor(monitoring):`, `docs:`, `chore(deps):`, `build(deps):`.
- Main branch is `develop`; PRs target it. CI runs ruff + pytest/coverage, dependency analysis, and
  gitleaks; GitHub Actions must be SHA-pinned.
- `.githooks/` holds pre-commit/pre-push dispatchers that run `gitleaks`. Never bypass them.
- File naming in `types/` is mostly snake_case (`host_group.py`) with one legacy exception
  (`monitoring/servicegroup.py`) — follow snake_case for new modules.
