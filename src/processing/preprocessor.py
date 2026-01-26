from sklearn.preprocessing import StandardScaler
import pandas as pd
from amountFeatures import AmountFeatures
from currencyFeatures import CurrencyFeatures
from datetimeFeatures import DatetimeFeatures
from velocityFeatures import VelocityFeatures

class TransactionPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()

    def get_amount_features(self, df: pd.DataFrame):
        amount_features = AmountFeatures(self.scaler)
        df = amount_features.normalize_amount(df)
        df = amount_features.add_raw_and_normalized_amount_features(df)
        df = amount_features.get_user_relative_features(df)
        return df

    def get_currency_features(self, df: pd.DataFrame):
        currency_features = CurrencyFeatures()
        df = currency_features.get_currency_features(df)
        return df
    
    def get_datetime_features(self, df: pd.DataFrame):
        datetime_features = DatetimeFeatures()
        df = datetime_features.get_datetime_features(df)
        return df
    
    def get_velocity_features(self, df: pd.DataFrame):
        velocity_features = VelocityFeatures()
        df = velocity_features.get_velocity_features(df)
        return df




