import pandas as pd

class TransactionTransformer:
    @staticmethod
    def to_dataframe(transactions):
        return pd.DataFrame(
            [{
                "transaction_id": t.transaction_id,
                "amount": t.amount,
                "currency": t.currency
            } for t in transactions]
        )
