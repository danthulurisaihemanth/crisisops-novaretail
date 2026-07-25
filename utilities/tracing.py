from typing import Callable, TypeVar

from config.settings import settings
from utilities.logging_config import LOGGER

try:
    from langsmith import traceable as langsmith_traceable
except Exception:  # pragma: no cover
    langsmith_traceable = None

F = TypeVar("F", bound=Callable)

def traceable(func: F) -> F:
    if settings.langsmith_tracing and langsmith_traceable is not None:
        return langsmith_traceable(func)  # type: ignore[return-value]
    return func

def trace_event(name: str, **payload: object) -> None:
    if settings.langsmith_tracing:
        LOGGER.info("trace:%s %s", name, payload)
