from typing import List

class KoinlyCustomTransaction:
    def __init__(self, id, date, operation) -> None:
        self.id = id
        self.date = date
        self.sent_amount = ""
        self.sent_currency = ""
        self.received_amount = ""
        self.received_currency = ""
        self.fee_amount = ""
        self.fee_currency = ""
        self.net_worth_amount = ""
        self.net_worth_currency = ""
        self.label = operation
        self.description = ""
        self.tx_hash = ""

    def serialize(self) -> str:
        return f'"{self.date}";{self.sent_amount};{self.sent_currency};{self.received_amount};{self.received_currency};{self.fee_amount};{self.fee_currency};{self.net_worth_amount};{self.net_worth_currency};{self.label};"{self.tx_hash}"'
    
    def set_amount(self, amount: float, currency: str):
        if amount < 0.0:
            self.sent_amount = abs(amount)
            self.sent_currency = currency
        else:
            self.received_amount = abs(amount)
            self.received_currency = currency

    def set_cost(self, amount: float, currency: str):
        if amount != 0.0:
            self.fee_amount = abs(amount)
            self.fee_currency = currency

class KoinlyCustomFile:
    def __init__(self) -> None:
        self.transactions: List[KoinlyCustomTransaction] = []

    def add_trx(self, trx: KoinlyCustomTransaction):
        self.transactions.append(trx)

    def write(self, filename: str):
        with open(filename, "w") as f:
            f.write("Date;Sent Amount;Sent Currency;Received Amount;Received Currency;Fee Amount;Fee Currency;Net Worth Amount;Net Worth Currency;Label;Description;TxHash\n")
            for trx in self.transactions:
                f.write(trx.serialize() + "\n")
        f.close()
