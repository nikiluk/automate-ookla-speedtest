"""
Run speedteset num_tests=10 times
Save all results in individual JSON files
Save separate CSV file
"""

import subprocess
import json
import pandas as pd
from datetime import datetime
import os

def run_speedtest():
    result = subprocess.run(['speedtest', '-f', 'json'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running speedtest: {result.stderr}")
        return None
    try:
        return json.loads(result.stdout)
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Raw output from speedtest command:\n{result.stdout}")
        return None


def flatten_json(json_data, parent_key='', separator='_'):
    flat_data = {}
    for key, value in json_data.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            flat_data.update(flatten_json(value, new_key, separator=separator))
        else:
            flat_data[new_key] = value
    return flat_data

def save_result_to_json(result, file_path):
    with open(file_path, 'w') as file:
        json.dump(result, file, indent=4)

def append_to_dataframe(result, dataframe):
    normalized_result = flatten_json(result)
    dataframe = dataframe.append(normalized_result, ignore_index=True)
    return dataframe

def main(num_tests=10):
    # Initialize an empty DataFrame
    df = pd.DataFrame()

    # Specify the folder path you want to create
    folder_path = 'results'

    # Check if the folder exists, and if not, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")

    for i in range(num_tests):
        print(f"Running Speed Test {i + 1}/{num_tests}")
        result = run_speedtest()
        flat_result = flatten_json(result)
        result_id = flat_result['result_id']
        save_result_to_json(result, os.path.join(folder_path, f'result_{result_id}.json'))
        result_df = pd.DataFrame([flat_result])
        df = pd.concat([df, result_df], ignore_index=True)
        print(flatten_json(result))

    df.set_index('result_id', inplace=True)
    df['download'] = df['download_bandwidth']*8/1000000
    df['upload'] = df['upload_bandwidth']*8/1000000
    df.to_csv(os.path.join(folder_path,'speedtest_results.csv'), index=True)
    print("Speed test results saved to 'speedtest_results.csv'.")

if __name__ == "__main__":
    main()
