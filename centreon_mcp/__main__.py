import asyncio
from contextlib import asynccontextmanager

from fastmcp import FastMCP
from httpx import AsyncClient

from centreon_mcp import auth, logger, settings
from centreon_mcp.components import components
from centreon_mcp.types.platform import Platform
from centreon_mcp.utils import request


@asynccontextmanager
async def lifespan(app: FastMCP):
    """
    Lifespan context manager for FastMCP application.
    """

    # Initialize Centreon client
    request.client = AsyncClient(verify=settings.verify, timeout=settings.client_timeout)
    logger.info(
        f"Centreon API Client initialized (\n"
        f"\ttimeout={settings.client_timeout},\n"
        f"\ttls_secure={settings.tls_secure},\n"
        f"\tca_bundle={settings.ca_bundle},\n"
        ")."
    )

    # Test Centreon API connectivity and get web version
    tenants = await auth.plugin.tenants()
    tasks = [asyncio.create_task(Platform.get_web_version(tenant)) for tenant in tenants]
    versions = await asyncio.gather(*tasks)

    for tenant, version in zip(tenants, versions):
        logger.info(f"Connected to Centreon API version {version.version} for {tenant.name}")

    yield

    # Close Centreon Client
    await request.client.aclose()


def main():

    # Set log level from environment variable
    logger.setLevel(settings.mcp_log_level)

    # Load auth plugin
    auth.load()

    # Instantiate mcp server with configured authentication
    mcp = FastMCP(name="Centreon MCP Server", auth=auth.plugin.provider(), lifespan=lifespan)

    # Import components
    [mcp.mount(server) for server in components]

    # Start Centreon MCP
    mcp.run(transport="http", host=settings.mcp_host, port=settings.mcp_port)
