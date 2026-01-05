from ..dataclasses.transaction import Transaction

class FraudDetection():
    def __init__(self, method, data):
        self.method = method
        self.data_df = data
        self.flagged_transactions = []

    def check(self):
        if self.method == "naive":
            for _, transaction in self.data_df.iterrows():
                print(transaction)
                if (checkBasicFilters(transaction)):
                    print("In flagged transactions")
                    self.flagged_transactions.append(transaction['transaction_id'])

    def get_flagged_transactions(self):
        return self.flagged_transactions

def checkBasicFilters(transaction):
    print('In Amount filter')
    print(transaction['amount'])
    if (transaction['amount']) <= 0:
        return True
    return False
        