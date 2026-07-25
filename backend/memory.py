from collections import defaultdict
from typing import Any, Dict, List

class ConversationMemory:
    def __init__(self) -> None:
        self.sessions: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.session_state: Dict[str, Dict[str, Any]] = {}

    def add_message(self, session_id: str, role: str, content: str) -> None:
        self.sessions[session_id].append({"role": role, "content": content})

    def get_history(self, session_id: str) -> List[Dict[str, Any]]:
        return self.sessions.get(session_id, [])

    def set_state(self, session_id: str, key: str, value: Any) -> None:
        self.session_state.setdefault(session_id, {})[key] = value

    def get_state(self, session_id: str, key: str, default: Any = None) -> Any:
        return self.session_state.get(session_id, {}).get(key, default)

    def clear(self, session_id: str) -> None:
        self.sessions.pop(session_id, None)
        self.session_state.pop(session_id, None)
