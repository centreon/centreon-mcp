"""
Tools reporting what the server is doing on behalf of the current user.
"""

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token
from pydantic import BaseModel, Field

from centreon_mcp import logger
from centreon_mcp.auth import AUTHENTICATED, AuthenticationError, Role, get_plugin

account = FastMCP()


class Context(BaseModel):
    """
    Which Centreon the server acts on, and with which permission level.
    """

    tenant: str | None = Field(
        description="Name of the Centreon the tools act on, null when none could be resolved"
    )
    role: str = Field(description="Permission level of the user: none, reader, editor or admin")
    authenticated: bool = Field(
        description="Whether the user signed in. False on a server that authenticates nobody, "
        "which is a normal configuration and not a problem to report"
    )
    detail: str | None = Field(
        None, description="Why no Centreon or no level could be resolved, when the server knows"
    )


@account.tool(
    annotations={
        "title": "Get the current context",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
    # Requires no permission level: a user granted none reaches no other tool, and this is what
    # tells them so
    auth=AUTHENTICATED,
)
async def get_current_context() -> Context:
    """
    Get the Centreon the tools act on and the permission level of the current user.
    Use it to tell users which platform they are working on, or to explain why a tool
    they expect is not available to them. A null `tenant` or a `role` of "none" means
    they reach nothing, and `detail` then carries the reason when the server knows one.
    """
    logger.info("Executing tool get_current_context")

    token = get_access_token()
    plugin = get_plugin()
    reasons = []

    # Explaining why nothing is available is this tool's job, so anything the plugin raises is
    # reported rather than propagated: failing here would leave the user with no answer at all
    try:
        tenant = (await plugin.tenant(token)).name
    except AuthenticationError as error:
        logger.info(f"No Centreon resolved for the current user: {error}")
        tenant = None
        reasons.append(str(error))
    except Exception as error:  # noqa: BLE001 — see above
        logger.error(f"Cannot resolve the Centreon of the current user: {error}", exc_info=True)
        tenant = None
        reasons.append("The server could not determine which Centreon you reach")

    try:
        role = await plugin.role(token)
    except AuthenticationError as error:
        logger.info(f"No level granted to the current user: {error}")
        role = Role.NONE
        reasons.append(str(error))
    except Exception as error:  # noqa: BLE001 — see above
        logger.error(f"Cannot resolve the role of the current user: {error}", exc_info=True)
        role = Role.NONE
        reasons.append("The server could not determine your permission level")

    return Context(
        tenant=tenant,
        role=role.name.lower(),
        authenticated=token is not None,
        detail=". ".join(reasons) or None,
    )
