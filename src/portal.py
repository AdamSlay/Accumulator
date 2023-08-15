import csv
import requests


def fetch_parm(parm: str):
    # Make a GET request to a URL
    parm = parm.strip().lower()
    tair_latest = f"http://portal.dev.okmeso.net/data/api/rest/times/latest?parm={parm}:fahr&fmt=csv"
    response = requests.get(tair_latest)

    # Check the response status code
    if response.status_code == 200:
        # Print the response content
        print(response.text)
        with open('../data/latest_tair.csv', 'w') as f:
            f.write(response.text)
    else:
        print("Request failed with status code:", response.status_code)
        print("\nResponse:", response.text)
