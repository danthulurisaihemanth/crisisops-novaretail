import random
from typing import Any, Dict, List

from config.settings import settings

class LLMService:
    def __init__(self) -> None:
        self.provider = "fallback"
        if settings.gemini_api_key:
            self.provider = "gemini"

    def generate(self, prompt: str, context: Dict[str, Any] | None = None) -> str:
        if self.provider == "gemini":
            return f"Gemini integration is configured with a key. Prompt: {prompt[:120]}"
        return self._fallback_response(prompt, context or {})

    def _fallback_response(self, prompt: str, context: Dict[str, Any]) -> str:
        lowered = prompt.lower()
        if "shipment" in lowered:
            return "I would inspect the shipment and impacted orders before recommending a recovery path."
        if "supplier" in lowered:
            return "I would compare active suppliers based on availability, lead time, and cost." 
        if "inventory" in lowered:
            return "I would review warehouse stock and reserve levels to identify the likely shortage."
        if "incident" in lowered:
            return "I would create a structured incident timeline and highlight business impact."
        return "I can help evaluate the operational impact and recommend the next best step."
