from typing import Any, Dict, List

from utilities.logging_config import LOGGER


class ToolError(Exception):
    pass


def validate_required(payload: Dict[str, Any], required_fields: List[str]) -> None:
    missing = [field for field in required_fields if not payload.get(field)]
    if missing:
        raise ToolError(f"Missing required fields: {', '.join(missing)}")


def log_tool_call(tool_name: str, **payload: Any) -> None:
    LOGGER.info("tool:%s %s", tool_name, payload)
