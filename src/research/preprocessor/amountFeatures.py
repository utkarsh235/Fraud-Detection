import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class AmountFeatures:
    def __init__(self, scaler=None):
        self.scaler = scaler if scaler is not None else StandardScaler()

    # --------------------------------------------------
    # Public APIs
    # --------------------------------------------------

    def normalize_amount(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["amount_normalized"] = self.scaler.fit_transform(
            df["amount"].values.reshape(-1, 1)
        )
        return df

    def add_raw_and_normalized_amount_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df = self._get_log_amount(df)
        df = self._get_amount_ranked_per_user(df)
        return df

    def get_user_relative_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        df['transaction_ts'] = pd.to_datetime(
            df['date_of_transaction'].astype(str) + ' ' +
            df['time_of_transaction'].astype(str)
        )

        df = df.sort_values(['user_id', 'transaction_ts'])

        df = self._get_user_rolling_average(df)
        df = self._get_amount_vs_user_average(df)
        df = self._get_amount_zscore_per_user(df)
        df = self._get_amount_percentile(df)

        return df

    # --------------------------------------------------
    # Private helpers
    # --------------------------------------------------

    def _get_user_rolling_average(self, df: pd.DataFrame) -> pd.DataFrame:
        df['user_avg_amount'] = (
            df.groupby('user_id')['amount']
              .expanding()
              .mean()
              .shift(1)  # past-only (NO leakage)
              .reset_index(level=0, drop=True)
        )
        return df

    def _get_amount_vs_user_average(self, df: pd.DataFrame) -> pd.DataFrame:
        df['amount_vs_user_avg'] = df['amount'] / df['user_avg_amount']
        df['amount_minus_user_avg'] = df['amount'] - df['user_avg_amount']
        return df

    def _get_amount_zscore_per_user(self, df: pd.DataFrame) -> pd.DataFrame:
        df['user_std_amount'] = (
            df.groupby('user_id')['amount']
              .expanding()
              .std()
              .shift(1)
              .reset_index(level=0, drop=True)
        )

        df['amount_zscore_user'] = (
            (df['amount'] - df['user_avg_amount']) / df['user_std_amount']
        )

        df['amount_zscore_user'] = df['amount_zscore_user'].replace(
            [np.inf, -np.inf], np.nan
        )

        return df

    def _get_amount_percentile(self, df: pd.DataFrame) -> pd.DataFrame:
        df['amount_percentile_user'] = (
            df.groupby('user_id')['amount']
              .expanding()
              .apply(lambda x: (x <= x.iloc[-1]).mean())
              .shift(1)
              .reset_index(level=0, drop=True)
        )
        return df

    def _get_log_amount(self, df: pd.DataFrame) -> pd.DataFrame:
        # safer than math.log(amount)
        df['log_amount'] = np.log(df['amount'] + 1)
        return df

    def _get_amount_ranked_per_user(self, df: pd.DataFrame) -> pd.DataFrame:
        df['amount_rank_user'] = (
            df.groupby('user_id')['amount']
              .expanding()
              .rank(pct=True)
              .shift(1)  # past-only
              .reset_index(level=0, drop=True)
        )
        return df
