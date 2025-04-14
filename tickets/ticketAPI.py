# # -------------------------------------------------------- #
# # Only run the API calls if you dont have the current data #
# # -------------------------------------------------------- #

import pandas as pd
import os
import requests


url = 'https://services1.arcgis.com/UWYHeuuJISiGmgXx/arcgis/rest/services/Finance_Parking_Fines/FeatureServer/0/query'

batch_size = 2000
offset = 0
data_list = []

params = {
    'where': '1=1',
    'outFields': '*',
    'returnGeometry': 'false',
    'f': 'json',
    'resultOffset': offset,
    'resultRecordCount': batch_size
}

while True:
    params['resultOffset'] = offset
    response = requests.get(url, params=params)

    print(f"Requesting URL: {response.url}")

    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        break

    try:
        query_result = response.json()
    except ValueError:
        print(f"Failed to parse JSON response: {response.text}")
        break

    features = query_result.get('features', [])

    if not features:
        break

    for feature in features:
        data_list.append(feature['attributes'])

    if len(features) < batch_size:
        break

    offset += batch_size

if data_list:
    df = pd.DataFrame(data_list)

    output_directory = 'data'

    os.makedirs(output_directory, exist_ok=True)

    output_path = os.path.join(output_directory, 'tickets.csv')
    df.to_csv(output_path, index=False)

    print(f"Data saved to {output_path}")
else:
    print("No data retrieved.")