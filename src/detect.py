import pandas as pd
from sklearn.preprocessing import StandardScaler
from .naive_fraud_detection.fraud_detection import FraudDetection
from .dataclasses.transaction import Transaction

def detect(data: list[Transaction]):
    print("Inside detect")
    # getdata
    # Validate and clean data
    validateData(data)
    df = transformData(data)
    # clean = cleanData(df)
    processed_df = preprocessing(df)
    # create request
    # call fraud detection
    fraud_detection = FraudDetection(method='naive', data=processed_df)
    fraud_detection.check()
    return fraud_detection.get_flagged_transactions()

def normalizeAmount(amount):
    ss = StandardScaler()
    amount = ss.fit_transform(amount.values.reshape(-1,1))
    return amount

def preprocessing(df):
    df['amount'] = normalizeAmount(df['amount'])
    return df

def transformData(data):
    print("In transform data")
    df = pd.DataFrame({
        'transaction_id': [],
        'amount': [],
        'currency': []
    })
    # df.columns = ['transaction_id', 'amount', 'currency']
    for transaction in data:
        len_df = df.shape[0]
        df.loc[len_df] = [
            transaction['transaction_id'],
            transaction['amount'],
            transaction['currency']
        ]
    print(df)
    return df
    

def validateData(data):
    for transaction in data:
        print("TRANSACTION => ", transaction)
        if (transaction['amount']) is not None and (transaction['transaction_id']) is not None:
            continue
        else: 
            raise Exception("Mandatory attribute missing for: " + transaction)
