import datetime
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
from dotenv import load_dotenv
import os

load_dotenv()

path = os.getenv("PATH_TO_SERVICE_ACCOUNT")
cred = credentials.Certificate(path)
firebase_admin.initialize_app(cred)
db = firestore.client()


def get_last_api_hit():
    result = db.collection("global-data").document("currency-rates").get().to_dict()
    return datetime.datetime.fromisoformat(result["last_api_hit"])
    
   
def update_api_data_into_firestore(data):
    db.collection("global-data").document("currency-rates").set(data)


def get_currency_rates_from_API():
    db.collection("global-data").document("currency-rates").update({"last_script_run": datetime.datetime.now().isoformat()})
    last_api_hit = get_last_api_hit()
    number_of_days = (datetime.datetime.now() - last_api_hit).days

    if number_of_days < 1:
        return "Next API hit at: {}".format((last_api_hit + datetime.timedelta(seconds=86400)).strftime("%A %d %b %Y %H:%M:%S %p"))

    print("Getting currency rates from API")
    URL = os.getenv("API_URL")
    print(URL)
    result = requests.get(URL).json()
    result['last_api_hit'] = datetime.datetime.now().isoformat()    
    result['last_script_run'] = datetime.datetime.now().isoformat()   
    country_currency_symbols = {
    "AD": "€", "AE": "د.إ", "AF": "؋", "AG": "$", "AI": "$", "AL": "L", "AM": "֏", "AO": "Kz", "AR": "$", "AS": "$",
    "AT": "€", "AU": "$", "AW": "ƒ", "AX": "€", "AZ": "₼", "BA": "KM", "BB": "$", "BD": "৳", "BE": "€", "BF": "Fr",
    "BG": "лв", "BH": ".د.ب", "BI": "Fr", "BJ": "Fr", "BL": "€", "BM": "$", "BN": "$", "BO": "Bs.", "BQ": "$", "BR": "R$",
    "BS": "$", "BT": "Nu.", "BV": "kr", "BW": "P", "BY": "Br", "BZ": "$", "CA": "$", "CC": "$", "CD": "Fr", "CF": "Fr",
    "CG": "Fr", "CH": "Fr", "CI": "Fr", "CK": "$", "CL": "$", "CM": "Fr", "CN": "¥", "CO": "$", "CR": "₡", "CU": "$",
    "CV": "$", "CW": "ƒ", "CX": "$", "CY": "€", "CZ": "Kč", "DE": "€", "DJ": "Fr", "DK": "kr", "DM": "$", "DO": "$",
    "DZ": "د.ج", "EC": "$", "EE": "€", "EG": "£", "EH": "د.م.", "ER": "Nfk", "ES": "€", "ET": "Br", "FI": "€", "FJ": "$",
    "FM": "$", "FO": "kr", "FR": "€", "GA": "Fr", "GB": "£", "GD": "$", "GE": "₾", "GF": "€", "GG": "£", "GH": "₵",
    "GI": "£", "GL": "kr", "GM": "D", "GN": "Fr", "GP": "€", "GQ": "Fr", "GR": "€", "GT": "Q", "GU": "$", "GW": "Fr",
    "GY": "$", "HK": "$", "HM": "$", "HN": "L", "HR": "kn", "HT": "G", "HU": "Ft", "ID": "Rp", "IE": "€", "IL": "₪",
    "IM": "£", "IN": "₹", "IO": "$", "IQ": "ع.د", "IR": "﷼", "IS": "kr", "IT": "€", "JE": "£", "JM": "$", "JO": "د.ا",
    "JP": "¥", "KE": "Sh", "KG": "сом", "KH": "៛", "KI": "$", "KM": "Fr", "KN": "$", "KP": "₩", "KR": "₩", "KW": "د.ك",
    "KY": "$", "KZ": "₸", "LA": "₭", "LB": "ل.ل", "LC": "$", "LI": "Fr", "LK": "රු", "LR": "$", "LS": "L", "LT": "€",
    "LU": "€", "LV": "€", "LY": "ل.د", "MA": "د.م.", "MC": "€", "MD": "L", "ME": "€", "MF": "€", "MG": "Ar", "MH": "$",
    "MK": "ден", "ML": "Fr", "MM": "Ks", "MN": "₮", "MO": "P", "MP": "$", "MQ": "€", "MR": "UM", "MS": "$", "MT": "€",
    "MU": "₨", "MV": "ރ", "MW": "MK", "MX": "$", "MY": "RM", "MZ": "MT", "NA": "$", "NC": "Fr", "NE": "Fr", "NF": "$",
    "NG": "₦", "NI": "C$", "NL": "€", "NO": "kr", "NP": "रू", "NR": "$", "NU": "$", "NZ": "$", "OM": "ر.ع.", "PA": "$",
    "PE": "S/", "PF": "Fr", "PG": "K", "PH": "₱", "PK": "₨", "PL": "zł", "PM": "€", "PN": "$", "PR": "$", "PT": "€",
    "PW": "$", "PY": "₲", "QA": "ر.ق", "RE": "€", "RO": "lei", "RS": "дин", "RU": "₽", "RW": "Fr", "SA": "ر.س", "SB": "$",
    "SC": "₨", "SD": "ج.س.", "SE": "kr", "SG": "$", "SH": "£", "SI": "€", "SJ": "kr", "SK": "€", "SL": "Le", "SM": "€",
    "SN": "Fr", "SO": "Sh", "SR": "$", "SS": "£", "ST": "Db", "SV": "$", "SX": "ƒ", "SY": "£", "SZ": "E", "TC": "$",
    "TD": "Fr", "TF": "€", "TG": "Fr", "TH": "฿", "TJ": "SM", "TK": "$", "TL": "$", "TM": "m", "TN": "د.ت", "TO": "T$",
    "TR": "₺", "TT": "$", "TV": "$", "TZ": "Sh", "UA": "₴", "UG": "Sh", "US": "$", "UY": "$", "UZ": "сўм", "VA": "€",
    "VC": "$", "VE": "Bs", "VG": "$", "VI": "$", "VN": "₫", "VU": "Vt", "WF": "Fr", "WS": "T", "YE": "﷼", "YT": "€",
    "ZA": "R", "ZM": "ZK", "ZW": "$"
    } 
    result['country_currency_symbols'] = country_currency_symbols
    update_api_data_into_firestore(result)
    print(result)
    return "Currency rates updated in Firestore at: " + result['last_api_hit']



