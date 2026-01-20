class TransactionValidator:
    @staticmethod
    def validate(transactions):
        for transaction in transactions:
            if transaction.transaction_id is None or transaction.amount is None:
                raise ValueError(
                    f"Mandatory attribute missing for transaction: {transaction}"
                )
