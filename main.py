import datetime
import time
import currency

def currency_rates():
    print(currency.get_currency_rates_from_API())
    time.sleep(5)

currency_rates()