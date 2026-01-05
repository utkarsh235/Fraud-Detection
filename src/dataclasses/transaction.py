from typing import Optional
from pydantic import BaseModel

class Transaction(BaseModel):
    """
    Represents a financial transaction.

    Attributes:
        transaction_id: A unique identifier for the transaction (str).
        amount: Notional value of the transaction (int).
        location: The location where the transaction occurred (str, optional).
        currency: The transaction currency (str, optional).
    """
    transaction_id: str
    amount: int
    location: Optional[str] = None
    currency: Optional[str] = None
