import pandas as pd
import numpy as np

class DatetimeFeatures():
    def __init__(self):
        pass

    def get_datetime_features(self, df):
        df = self._add_basic_time_features(df)
        df = self._add_cyclical_time_features(df)
        df = self._add_user_time_features(df)
        return df

    def _add_basic_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
    
        ts = df['transaction_ts']
    
        df['hour_of_day'] = ts.dt.hour
        df['minute_of_hour'] = ts.dt.minute
        df['day_of_week'] = ts.dt.dayofweek      # 0=Mon
        df['day_of_month'] = ts.dt.day
        df['week_of_year'] = ts.dt.isocalendar().week.astype(int)
        df['month'] = ts.dt.month
        df['year'] = ts.dt.year
    
        df['is_weekend'] = ts.dt.dayofweek.isin([5, 6]).astype(int)
        df['is_night_txn'] = ts.dt.hour.between(0, 5).astype(int)
    
        return df

    def _add_cyclical_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
    
        df['hour_sin'] = np.sin(2 * np.pi * df['hour_of_day'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour_of_day'] / 24)
    
        df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
        df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
    
        return df

    def _add_user_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df = df.sort_values(['user_id', 'transaction_ts'])
    
        df['time_since_last_txn_user'] = (
            df.groupby('user_id')['transaction_ts']
              .diff()
              .dt.total_seconds()
        )
    
        df['avg_time_between_txns_user'] = (
            df.groupby('user_id')['time_since_last_txn_user']
              .expanding()
              .mean()
              .shift(1)
              .reset_index(level=0, drop=True)
        )
    
        return df
