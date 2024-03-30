from typing import List

class KoinlyCustomTransaction:
    def __init__(self, id, date, operation, txhash="") -> None:
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
        self.tx_hash = txhash
        self.currencyhelper = CurrencyHelper()

    def serialize(self) -> str:
        return f'"{self.date}";{self.sent_amount};{self.sent_currency};{self.received_amount};{self.received_currency};{self.fee_amount};{self.fee_currency};{self.net_worth_amount};{self.net_worth_currency};{self.label};"{self.description}";"{self.tx_hash}"'
    
    def set_amount(self, amount: float, currency: str):
        currency = self.currencyhelper.symbol2id(currency)
        
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
        self.columns = ["Date", "Sent Amount", "Sent Currency", "Received Amount", "Received Currency", "Fee Amount", "Fee Currency", "Net Worth Amount",
                        "Net Worth Currency", "Label", "Description", "TxHash"]

    def add_trx(self, trx: KoinlyCustomTransaction):
        self.transactions.append(trx)

    def write(self, filename: str):
        with open(filename, "w") as f:
            f.write(";".join(self.columns) + "\n")
            for trx in self.transactions:
                f.write(trx.serialize() + "\n")
        f.close()

class CurrencyHelper:
    CURRENCY_MAP = {"ARS": "3622"}

    def symbol2id(self, currency):
        if currency in self.CURRENCY_MAP:
            return "ID:" + self.CURRENCY_MAP[currency]
        else:
            return currency

