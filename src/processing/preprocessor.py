from sklearn.preprocessing import StandardScaler
import pandas as pd
from amountFeatures import AmountFeatures

class TransactionPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()

    def get_amount_features(self, df: pd.DataFrame):
        amount_features = AmountFeatures(self.scaler)
        df = amount_features.normalize_amount(df)
        df = amount_features.add_raw_and_normalized_amount_features(df)
        df = amount_features.get_user_relative_features(df)
        return df
