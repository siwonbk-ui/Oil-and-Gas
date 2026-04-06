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
    Fetches real oil prices for Thailand via Bangchak API.
    Other countries remain simulated for now.
    """
    from datetime import datetime, timezone, timedelta
    import urllib.request
    
    # Use UTC+7 (Thailand Time) to ensure the date matches the local time when the job runs at 05:00 AM
    tz = timezone(timedelta(hours=7))
    today = datetime.now(tz).strftime("%Y-%m-%d")
    data['last_updated'] = today
    
    # Fetch actual Thailand prices from Bangchak API
    thailand_real = {'gasoline': None, 'diesel': None}
    try:
        req = urllib.request.Request("https://www.bangchak.co.th/api/oilprice", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                bc_data = json.loads(response.read().decode('utf-8'))
                for item in bc_data.get('data', {}).get('items', []):
                    if item.get('OilName') == 'แก๊สโซฮอล์ 95 S EVO':
                        thailand_real['gasoline'] = item.get('PriceToday')
                    elif item.get('OilName') == 'ไฮดีเซล S':
                        thailand_real['diesel'] = item.get('PriceToday')
    except Exception as e:
        print(f"Failed to fetch Bangchak API: {e}")
        # fallback to simulation if fails
    
    for fuel_type in ['gasoline', 'diesel']:
        # Dynamically generate 30 dates for the labels
        labels = [(datetime.now(tz) - timedelta(days=i)).strftime("%b %d") for i in range(29, -1, -1)]
        data[fuel_type]['history']['labels'] = labels
        
        for i, card in enumerate(data[fuel_type]['cards']):
            
            if card['code'] == 'TH' and thailand_real[fuel_type] is not None:
                new_price = round(float(thailand_real[fuel_type]), 2)
                change = round(new_price - card['price'], 2)
                card['price'] = new_price
                card['change'] = f"{change:+.2f}"
            else:
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
            history_dataset = next(d for d in data[fuel_type]['history']['datasets'] if d['label'] == card['country'])
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
