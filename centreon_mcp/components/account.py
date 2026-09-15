"""
Tools reporting what the server is doing on behalf of the current user.
"""

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token
from pydantic import BaseModel

from centreon_mcp.auth import AUTHENTICATED, AuthenticationError, Role, get_plugin
from centreon_mcp.utils import logger

account = FastMCP()


class Context(BaseModel):
    """
    Which Centreon the server acts on, and with which permission level.
    """

    tenant: str | None
    role: str
    authenticated: bool
    detail: str | None = None


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
    they expect is not available to them. When `tenant` is null or `role` is "none",
    `detail` carries the reason, which is what the user has to act on.
    """
    logger.info("Executing tool get_current_context")

    token = get_access_token()
    plugin = get_plugin()
    reasons = []

    # Explaining why nothing is available is this tool's job, so a Centreon or a level that
    # cannot be resolved is reported rather than raised
    try:
        tenant = (await plugin.tenant(token)).name
    except AuthenticationError as error:
        tenant = None
        reasons.append(str(error))

    try:
        role = await plugin.role(token)
    except AuthenticationError as error:
        role = Role.NONE
        reasons.append(str(error))

    return Context(
        tenant=tenant,
        role=role.name.lower(),
        authenticated=token is not None,
        detail=". ".join(reasons) or None,
    )
