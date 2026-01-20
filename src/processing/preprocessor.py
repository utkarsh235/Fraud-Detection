from sklearn.preprocessing import StandardScaler

class TransactionPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()

    def normalize_amount(self, df):
        df["amount"] = self.scaler.fit_transform(
            df["amount"].values.reshape(-1, 1)
        )
        return df
