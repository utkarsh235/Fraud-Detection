import pandas as pd
from src.domain.transaction import Transaction

class TransactionTransformer:
    @staticmethod
    def to_dataframe(transactions: list[Transaction]):
        return pd.DataFrame(
            [{
                "transaction_id": t.transaction_id,
                "user_id": t.user_id,
                "amount": t.amount,
                "currency": t.currency,
                "date": t.date,
                "time": t.time
            } for t in transactions]
        )
