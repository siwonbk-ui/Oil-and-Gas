import json
import random
import datetime
import os

# This script simulates an API fetch and updates data.json
FILE_PATH = 'data.json'

def load_data():
    if not os.path.exists(FILE_PATH):
        raise FileNotFoundError(f"{FILE_PATH} does not exist.")
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def fetch_real_prices(data):
    """
    STUB: In a real world scenario, you would implement web scraping 
    or API calls here. e.g. querying EPPO Thailand or GlobalPetrolPrices.
    For this automation demo, we simulate a slight market fluctuation.
    """
    today = datetime.date.today().strftime("%Y-%m-%d")
    data['last_updated'] = today
    
    for fuel_type in ['gasoline', 'diesel']:
        for i, card in enumerate(data[fuel_type]['cards']):
            # Simulate a small price variation between -0.40 and +0.40 THB
            change = round(random.uniform(-0.4, 0.4), 2)
            card['price'] = round(card['price'] + change, 2)
            card['change'] = f"{change:+.2f}"
            
            if change > 0:
                card['trend'] = 'up'
            elif change < 0:
                card['trend'] = 'down'
            else:
                card['trend'] = 'flat'
            
            # Update the historical chart
            # Find the corresponding dataset by country code/label
            history_dataset = data[fuel_type]['history']['datasets'][i]
            history_data = history_dataset['data']
            
            # Shift left (remove oldest day) and append today's new price
            history_data.pop(0)
            history_data.append(card['price'])

            # Round datasets to avoid floating point anomalies in json
            history_dataset['data'] = [round(v, 2) for v in history_data]

    return data

if __name__ == "__main__":
    print("Starting automated oil price fetch process...")
    try:
        current_data = load_data()
        updated_data = fetch_real_prices(current_data)
        save_data(updated_data)
        print(f"Successfully updated data.json for {updated_data['last_updated']}")
    except Exception as e:
        print(f"Error during update: {e}")
