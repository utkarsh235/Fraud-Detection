from dataclasses import dataclass
from typing import Optional

@dataclass
class Transaction:
    transaction_id: str
    user_id: str
    amount: float
    currency: str
    date: Optional[str]
    time: Optional[str]
