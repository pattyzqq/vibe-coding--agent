import json
import os
from typing import List, Dict, Any

class HardwareManager:
    def __init__(self):
        self.components_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "components.json")
        self.components = self._load_components()

    def _load_components(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.components_path):
            return []
        with open(self.components_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_component(self, name: str) -> Dict[str, Any]:
        for comp in self.components:
            if comp["name"] == name:
                return comp
        return None

    def get_all_components(self) -> List[Dict[str, Any]]:
        return self.components

hardware_mgr = HardwareManager()
