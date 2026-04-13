import json
import os

def fix_data():
    file_path = 'data.json'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Update Thailand Diesel Current Price
    th_diesel_card = next(c for c in data['diesel']['cards'] if c['code'] == 'TH')
    old_price = th_diesel_card['price']
    th_diesel_card['price'] = 44.4
    th_diesel_card['change'] = "+0.00"
    th_diesel_card['trend'] = 'flat'
    
    print(f"Updated Thailand Diesel price: {old_price} -> 44.4")

    # 2. Fix History for Thailand Diesel
    th_history = next(d for d in data['diesel']['history']['datasets'] if d['label'] == 'Thailand')
    prices = th_history['data']
    
    # Indices 23 to 26 (Apr 05 to Apr 08) were ~48-50 THB (Premium prices)
    # We'll fix them to 33.00 (Standard)
    for i in range(23, 27):
        if i < len(prices):
            print(f"Fixing history index {i}: {prices[i]} -> 33.0")
            prices[i] = 33.0
            
    # Also fix indices 10 to 22 which were also high (Apr 01 something)
    # Actually, let's look at the data again.
    # 514: 50.54 (Index 10 is Mar 23? No, Index 0 is Mar 13. Index 10 is Mar 23)
    # 513: 44.24 (Mar 22)
    # 514: 50.54 (Mar 23) -> This looks like when it started picking up premium.
    
    for i in range(11, 28): # Mar 24 to Apr 09
        if i < len(prices):
            if prices[i] > 45.0:
                print(f"Fixing history index {i}: {prices[i]} -> 33.0")
                prices[i] = 33.0

    # 3. Update Trends TH if necessary
    if 'trends_th' in data:
        data['trends_th']['last_known_prices']['diesel'] = 44.4

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Success: data.json fixed.")

if __name__ == '__main__':
    fix_data()
