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
    last_api_hit = get_last_api_hit()
    number_of_days = (datetime.datetime.now() - last_api_hit).days

    if number_of_days < 1:
        return "Next API hit at: {}".format((last_api_hit + datetime.timedelta(seconds=86400)).strftime("%A %d %b %Y %H:%M:%S %p"))

    print("Getting currency rates from API")
    URL = os.getenv("API_URL")
    print(URL)
    result = requests.get(URL).json()
    result['last_api_hit'] = datetime.datetime.now().isoformat()    
    update_api_data_into_firestore(result)
    print(result)
    return "Currency rates updated in Firestore at: " + result['last_api_hit']



