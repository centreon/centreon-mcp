import importlib
import pkgutil

from centreon_mcp import types
from centreon_mcp.utils.base import BaseFilter


def filter_classes() -> list[type[BaseFilter]]:
    """
    Import every `centreon_mcp.types` module and return all the `BaseFilter` subclasses it defines.

    Classes declared elsewhere, such as test-local filters, are left out so the result does not
    depend on the order the tests run in.
    """
    for module in pkgutil.walk_packages(types.__path__, f"{types.__name__}."):
        importlib.import_module(module.name)
    classes, pending = [], list(BaseFilter.__subclasses__())
    while pending:
        cls = pending.pop()
        pending.extend(cls.__subclasses__())
        if cls.__module__.startswith(f"{types.__name__}."):
            classes.append(cls)
    return sorted(classes, key=lambda cls: cls.__qualname__)
