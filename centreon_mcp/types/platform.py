from pydantic import BaseModel

from centreon_mcp.utils.request import request


class Version(BaseModel):
    version: str
    major: str
    minor: str
    fix: str


class Platform(BaseModel):
    @staticmethod
    async def get_web_version() -> Version:
        """
        Get platform web version.
        """
        content = await request("GET", "platform/versions")
        return Version(**content["web"])
