import json

file_path = 'data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. Rebuild History Array for Thailand Diesel
# We want to match the historical milestones we discovered.
# Initial price before Mar 18 was ~30.00
history_labels = data['diesel']['history']['labels']
th_diesel_ds = next(ds for ds in data['diesel']['history']['datasets'] if ds['label'] == 'Thailand')
new_history = []

current_p = 30.00
price_map = {
    'Mar 15': 30.00,
    'Mar 16': 30.00,
    'Mar 17': 30.00,
    'Mar 18': 30.50, # +0.50
    'Mar 19': 30.50,
    'Mar 20': 30.50,
    'Mar 21': 31.20, # +0.70
    'Mar 22': 31.20,
    'Mar 23': 31.20,
    'Mar 24': 33.00, # +1.80
    'Mar 25': 33.00,
    'Mar 26': 39.00, # +6.00
    'Mar 27': 39.00,
    'Mar 28': 39.00,
    'Mar 29': 39.00,
    'Mar 30': 39.00,
    'Mar 31': 40.80, # +1.80
    'Apr 01': 40.80,
    'Apr 02': 44.30, # +3.50
    'Apr 03': 47.80, # +3.50
    'Apr 04': 47.80,
    'Apr 05': 50.60, # +2.80
    'Apr 06': 50.60,
    'Apr 07': 50.60,
    'Apr 08': 50.60,
    'Apr 09': 48.40, # -2.20
    'Apr 10': 48.40,
    'Apr 11': 44.40, # -4.00
    'Apr 12': 44.40,
    'Apr 13': 44.40
}

for label in history_labels:
    new_history.append(price_map.get(label, 44.40))

th_diesel_ds['data'] = new_history

# 2. Rebuild Trends Table (Only entries with changes)
new_table = [
    {"date": "18 มี.ค. 69", "gasoline": 0.50, "e20": 0.50, "e85": 0.50, "diesel": 0.50},
    {"date": "21 มี.ค. 69", "gasoline": 0.70, "e20": 0.70, "e85": 0.70, "diesel": 0.70},
    {"date": "24 มี.ค. 69", "gasoline": 1.80, "e20": 1.80, "e85": 1.80, "diesel": 1.80},
    {"date": "26 มี.ค. 69", "gasoline": 6.00, "e20": 6.00, "e85": 6.00, "diesel": 6.00},
    {"date": "31 มี.ค. 69", "gasoline": 1.80, "e20": 1.80, "e85": 1.80, "diesel": 1.80},
    {"date": "2 เม.ย. 69", "gasoline": 1.20, "e20": 1.20, "e85": 1.20, "diesel": 3.50},
    {"date": "3 เม.ย. 69", "gasoline": 0.70, "e20": 0.70, "e85": 0.70, "diesel": 3.50},
    {"date": "5 เม.ย. 69", "gasoline": 0.00, "e20": 0.00, "e85": 0.00, "diesel": 2.80},
    {"date": "9 เม.ย. 69", "gasoline": 0.00, "e20": 0.00, "e85": 0.00, "diesel": -2.20},
    {"date": "11 เม.ย. 69", "gasoline": -1.00, "e20": -1.00, "e85": -1.00, "diesel": -4.00}
]

data['trends_th']['table_data'] = new_table
data['trends_th']['last_known_prices']['diesel'] = 44.40

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Final history and trends table reconstruction complete.")
