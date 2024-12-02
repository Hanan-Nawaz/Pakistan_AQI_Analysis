import requests as req
from dotenv import load_dotenv
import os
import pandas as pd

def configure():
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path)
    print(os.getenv('base_url'))

# first element is latitude and second is longitude
city_data = {
    "Lahore": [31.5204, 74.3587],
    "Karachi": [24.8607, 67.0011],
    "Islamabad": [33.6995, 73.0363],
    "Quetta": [30.1834, 66.9987],
    "Peshawar": [34.0151, 71.5249]
    }

def get_data_json(city):
    api_url = f'{os.getenv('base_url')}lat={city_data[city][0]}&lon={city_data[city][1]}&appid={os.getenv('api_key')}'
    print(api_url)
    try:
        print(f"--Loading--{city}_Data")
        response = req.get(api_url)
        response.raise_for_status()
        return response.json()
    
    except req.exceptions.ConnectionError:
        print("Error: Failed to connect to the server. Check your internet connection or URL.")
    except req.exceptions.Timeout:
        print("Error: The request timed out. The server might be too slow or unresponsive.")
    except req.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  
    except req.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}") 
    return None

def main():
    configure()
    keys = list(city_data.keys())
    for i in range(0, 5):
        data = get_data_json(keys[i])
        df = pd.json_normalize(data, sep="_")
        df.to_csv(f"extracted_data/{keys[i]}_data.csv")
        print(f"Extraction for {keys[i]} Completed!")
        if i == 4:
            print("Extraction phase completed!")

if __name__ == "__main__":
    main()

