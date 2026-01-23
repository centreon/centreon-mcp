import logging
from enum import Enum

from centreon_mcp import CREDENTIALS

logger = logging.getLogger("centreon-mcp")

# Set log level from environment variable
level = CREDENTIALS["CENTREON_MCP_LOG_LEVEL"]
try:
    logger.setLevel(level)
except Exception:
    logger.setLevel(logging.INFO)
    logger.warning(f"Invalid log level '{level}' set. Defaulting to INFO.")


class COLOR(str, Enum):
    GREY = "\033[90m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"

    def __str__(self):
        return self.value


class CustomFormatter(logging.Formatter):
    colors = {
        logging.DEBUG: COLOR.GREY,
        logging.INFO: COLOR.GREEN,
        logging.WARNING: COLOR.YELLOW,
        logging.ERROR: COLOR.RED,
    }

    def __init__(self) -> None:
        super().__init__(
            fmt="%(asctime)s  %(levelname)-10s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def format(self, record):
        color = self.colors.get(record.levelno, COLOR.RESET)
        record.levelname = f"{color}{record.levelname.ljust(8)}{COLOR.RESET}"
        record.msg = f"{color}{record.msg}{COLOR.RESET}"
        return super().format(record)


# Create custom formatter
formatter = CustomFormatter()

# Create a stream handler with the custom formatter
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)
