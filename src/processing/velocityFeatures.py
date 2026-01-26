import pandas as pd
import numpy as np

class VelocityFeatures():
    def __init__(self):
        pass

    def get_velocity_features(self, df):
        df = self._prepare_for_velocity(df)
        df = self._add_time_gap_features(df)
        df = self._add_transaction_count_velocity(df)
        df = self._add_amount_velocity(df)
        df = self._add_recent_transaction_gap_features(df)
        return df

    def _prepare_for_velocity(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df = df.sort_values(['user_id', 'transaction_ts'])
        return df

    def _add_time_gap_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
    
        df['time_since_last_txn_user'] = (
            df.groupby('user_id')['transaction_ts']
              .diff()
              .dt.total_seconds()
        )
        return df

    def _add_transaction_count_velocity(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df = df.sort_values(['user_id', 'transaction_ts'])
    
        df.set_index('transaction_ts', inplace=True)
    
        for window in ['5min', '1H', '24H']:
            df[f'txn_count_user_last_{window}'] = (
                df.groupby('user_id')
                  .rolling(window)
                  .size()
                  .shift(1)   # past-only
                  .reset_index(level=0, drop=True)
            )
    
        df.reset_index(inplace=True)
        return df

    def _add_amount_velocity(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df = df.sort_values(['user_id', 'transaction_ts'])
    
        df.set_index('transaction_ts', inplace=True)
    
        windows = ['1H', '24H']
    
        for window in windows:
            df[f'sum_amount_user_last_{window}'] = (
                df.groupby('user_id')['amount']
                  .rolling(window)
                  .sum()
                  .shift(1)
                  .reset_index(level=0, drop=True)
            )
    
            df[f'max_amount_user_last_{window}'] = (
                df.groupby('user_id')['amount']
                  .rolling(window)
                  .max()
                  .shift(1)
                  .reset_index(level=0, drop=True)
            )
    
        df.reset_index(inplace=True)
        return df

    def _add_recent_transaction_gap_features(self, df: pd.DataFrame, n=5) -> pd.DataFrame:
        df = df.copy()
        df = df.sort_values(['user_id', 'transaction_ts'])
    
        df[f'min_time_gap_user_last_{n}_txns'] = (
            df.groupby('user_id')['transaction_ts']
              .apply(lambda x: x.diff().dt.total_seconds().rolling(n).min())
              .shift(1)
              .reset_index(level=0, drop=True)
        )
    
        return df
