import pandas as pd
import numpy as np

class CurrencyFeatures():
    def __init__(self):
        pass

    def get_currency_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        df['transaction_ts'] = pd.to_datetime(
            df['date_of_transaction'].astype(str) + ' ' +
            df['time_of_transaction'].astype(str)
        )

        df = df.sort_values(['user_id', 'transaction_ts'])

        df = self._is_new_currency_for_user(df)
        df = self._currency_transaction_counts(df)
        df = self._currency_diversity(df)
        df = self._rolling_unique_currencies(df, window='7D')

        return df
    
    def _is_new_currency_for_user(self, df: pd.DataFrame) -> pd.DataFrame:
        df['is_new_currency_for_user'] = (
            df.groupby('user_id')['currency']
              .apply(lambda x: ~x.duplicated())
              .astype(int)
              .shift(1)  # past-only
              .reset_index(level=0, drop=True)
        )
        return df
    
    def _currency_transaction_counts(self, df: pd.DataFrame) -> pd.DataFrame:
        # count of this currency for user (past only)
        df['currency_txn_count_user'] = (
            df.groupby(['user_id', 'currency'])
              .cumcount()
        )

        # total txns per user (past only)
        df['total_txn_count_user'] = (
            df.groupby('user_id')
              .cumcount()
        )

        df['currency_txn_ratio_user'] = (
            df['currency_txn_count_user'] /
            df['total_txn_count_user'].replace(0, np.nan)
        )

        return df
    
    def _currency_diversity(self, df: pd.DataFrame) -> pd.DataFrame:
        # number of unique currencies used so far
        df['num_unique_currencies_user'] = (
            df.groupby('user_id')['currency']
              .apply(lambda x: (~x.duplicated()).cumsum())
              .shift(1)
              .reset_index(level=0, drop=True)
        )

        df['currency_diversity_user'] = (
            df['num_unique_currencies_user'] /
            df['total_txn_count_user'].replace(0, np.nan)
        )

        return df
    
    def _rolling_unique_currencies(self, df: pd.DataFrame, window='7D') -> pd.DataFrame:
        df.set_index('transaction_ts', inplace=True)

        df[f'num_unique_currencies_user_last_{window}'] = (
            df.groupby('user_id')['currency']
              .apply(lambda x: (~x.duplicated()).rolling(window).sum())
              .shift(1)
              .reset_index(level=0, drop=True)
        )

        df.reset_index(inplace=True)
        return df
    