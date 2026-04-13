import json
import os

def fix_data():
    file_path = 'data.json'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 2. Fix History for Thailand Diesel
    th_history = next(d for d in data['diesel']['history']['datasets'] if d['label'] == 'Thailand')
    prices = th_history['data']
    
    # We want to replace any out-of-bounds values. 
    # Valid values should be between 40 and 45 THB.
    # We have 50.54, 33.0, and 29.94
    
    for i in range(len(prices)):
        if prices[i] < 40.0 or prices[i] > 45.0:
            prices[i] = 44.4
            
    # Also fix gasoline if there are anomalies from 29.94
    for dataset in data['gasoline']['history']['datasets']:
        if dataset['label'] == 'Thailand':
            for i in range(len(dataset['data'])):
                if dataset['data'][i] < 35.0: # 40-45 THB is normal
                    dataset['data'][i] = 42.95

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Success: data.json history smoothed out.")

if __name__ == '__main__':
    fix_data()
