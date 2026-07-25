from typing import Any, Dict, Optional

from backend.memory import ConversationMemory

class HumanLoopManager:
    def __init__(self, memory: ConversationMemory) -> None:
        self.memory = memory

    def request_confirmation(self, session_id: str, action: str, payload: Dict[str, Any]) -> str:
        self.memory.set_state(session_id, "pending_action", {"action": action, "payload": payload})
        return f"I can {action} for you. Please confirm before I proceed."

    def get_pending_action(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self.memory.get_state(session_id, "pending_action")

    def clear_pending_action(self, session_id: str) -> None:
        self.memory.set_state(session_id, "pending_action", None)
