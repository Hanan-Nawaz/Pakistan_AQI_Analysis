import requests as req
from dotenv import load_dotenv
import os
import pandas as pd

def configure():
    """
    load data from .env file
    """

    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path)

# first element is latitude and second is longitude
city_data = {
    "Lahore": [31.5204, 74.3587],
    "Karachi": [24.8607, 67.0011],
    "Islamabad": [33.6995, 73.0363],
    "Quetta": [30.1834, 66.9987],
    "Peshawar": [34.0151, 71.5249]
    }

def get_data_json(city):
    """
    api_call code here.
    """

    api_url = f'{os.getenv('base_url')}lat={city_data[city][0]}&lon={city_data[city][1]}&appid={os.getenv('api_key')}'
    try:
        print(f"\n --Loading--{city}_Data \n")
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

def extract():
    """
    extract code here.
    """

    keys = list(city_data.keys())
    data_list = []

    for i in range(0, 5):
        data = get_data_json(keys[i])
        data_list.append(data)

        """
        As the range start from 0, that is the reason, I added (i + 1) below, so i will be 0 , 1, 2, 3, 4
        and when i is 0, 0+1 = 1 and when lahore's data is added, length of data_list is 1, so, it prints 
        the statement, else breaks. 
        """

        if len(data_list) == (i + 1):
            print(f" \n Extraction for {keys[i]} Completed! \n")
        else:
            print(f"\n Extraction for {keys[i]} Failed! Please Start Again")
            break
    
    return data_list

def transform(data_json_list):
    """
    transform code here.
    """

    print("\n Transformation phase Started! \n")

    df_each = [pd.json_normalize(item['list']) for item in data_json_list]
    df_data =  pd.concat(df_each, ignore_index=True)
    df_data = (item['coord'] for item in data_json_list)

    df_data.to_csv('data.csv')

def main():
    configure()

    data_json_list = extract()
    if len(data_json_list) == 5:
        print("\n Extraction phase completed! \n")
        transform(data_json_list)

if __name__ == "__main__":
    main()

