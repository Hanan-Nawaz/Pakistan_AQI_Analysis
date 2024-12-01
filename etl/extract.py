import requests as req
import time
from dotenv import load_dotenv
import os
import pandas as pd

def configure():
    load_dotenv()

# first element is latitude and second is longitude
city_data = {
    "Lahore": [31.5497, 74.3436],
    "Karachi": [24.8607, 67.0011],
    "Islamabad": [33.6844, 73.0479],
    "Quetta": [30.1798, 66.9750],
    "Peshawar": [34.0151, 71.5249]
    }

unix_timestamp = int(time.time())

def get_data_json():
    result = req.get(f'{os.getenv('api_url')}lat={city_data["Lahore"][0]}&lon={city_data["Lahore"][1]}&start={os.getenv('start_date')}&end={unix_timestamp}&appid={os.getenv('api_key')}')
    return result.json()

def main():
    configure()
    

if __name__ == "__main__":
    main()

