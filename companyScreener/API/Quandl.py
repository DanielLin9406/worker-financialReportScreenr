import os
import quandl
from dotenv import load_dotenv
load_dotenv()
quandl.ApiConfig.api_key = os.getenv("QUANDL_API_KEY")


def getTreasuriesYield():
    return quandl.get("ML/AAAEY").sort_index(ascending=False)
