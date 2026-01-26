import os
import pandas as pd

class TransactionRepository:
    def __init__(self, path: str):
        self.path = path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.isfile(self.path):
            df = pd.DataFrame(columns=["transaction_id", "user_id", "amount", "currency", "date", "time"])
            df.to_csv(self.path, index=False)

    def save(self, df: pd.DataFrame):
        existing = pd.read_csv(self.path)
        combined = pd.concat([existing, df], ignore_index=True)
        combined.to_csv(self.path, index=False)

    def find_all(self) -> pd.DataFrame:
        return pd.read_csv(self.path)
