import json
import os
from typing import Optional


class FeatureStore:
    def __init__(self, store_path: Optional[str] = None):
        self.store_path = store_path
        self.entries: dict[str, dict] = {}

    def load(self):
        if not self.store_path or not os.path.exists(self.store_path):
            return
        self.entries = {}
        with open(self.store_path, "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line)
                self.entries[item["user_id"]] = item

    def save(self):
        if not self.store_path:
            return
        os.makedirs(os.path.dirname(self.store_path), exist_ok=True)
        with open(self.store_path, "w", encoding="utf-8") as f:
            for entry in self.entries.values():
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def add(self, user_id: str, labels: dict[str, str], features: dict[str, str]):
        self.entries[user_id] = {
            "user_id": user_id,
            "label": labels,
            "features": features,
        }

    def get(self, user_id: str) -> Optional[dict]:
        return self.entries.get(user_id)

    def get_all(self) -> list[dict]:
        return list(self.entries.values())

    def __len__(self):
        return len(self.entries)
