from src.processing.validator import TransactionValidator
from src.processing.transformer import TransactionTransformer
from src.processing.preprocessor import TransactionPreprocessor
from src.repository.transaction_repository import TransactionRepository
from src.naive_fraud_detection.fraud_detection import FraudDetection

class FraudService:
    def __init__(self, transaction_path: str):
        self.repository = TransactionRepository(transaction_path)
        self.preprocessor = TransactionPreprocessor()

    def detect(self, transactions):
        # 1. Validate
        TransactionValidator.validate(transactions)

        # 2. Transform
        df = TransactionTransformer.to_dataframe(transactions)

        # 3. Persist
        self.repository.save(df)

        # 4. Load all historical data
        all_transactions = self.repository.find_all()

        # 5. Preprocess
        processed_df = self.preprocessor.normalize_amount(all_transactions)

        # 6. Detect fraud
        fraud_detection = FraudDetection(
            method="naive",
            data=processed_df
        )
        fraud_detection.check()

        return fraud_detection.get_flagged_transactions()
