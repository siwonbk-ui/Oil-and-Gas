import json

file_path = 'data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Rebuild Trends Table with real E20/E85 divergence
# Milestones for D, G, E20, E85
new_table = [
    {"date": "18 มี.ค. 69", "diesel": 0.50, "gasoline": 0.60, "e20": 0.60, "e85": 0.60},
    {"date": "21 มี.ค. 69", "diesel": 0.70, "gasoline": 1.00, "e20": 1.00, "e85": 1.00},
    {"date": "24 มี.ค. 69", "diesel": 1.80, "gasoline": 2.00, "e20": 2.00, "e85": 2.00},
    {"date": "26 มี.ค. 69", "diesel": 6.00, "gasoline": 6.00, "e20": 6.00, "e85": 6.00},
    {"date": "31 มี.ค. 69", "diesel": 1.80, "gasoline": 1.00, "e20": 1.00, "e85": 1.00},
    {"date": "2 เม.ย. 69", "diesel": 3.50, "gasoline": 1.20, "e20": 1.20, "e85": 1.20},
    {"date": "3 เม.ย. 69", "diesel": 3.50, "gasoline": 0.70, "e20": 0.70, "e85": 0.70},
    {"date": "5 เม.ย. 69", "diesel": 2.80, "gasoline": 0.00, "e20": -0.80, "e85": 0.00}, # Diverging E20
    {"date": "9 เม.ย. 69", "diesel": -2.20, "gasoline": 0.00, "e20": 0.00, "e85": 0.00},
    {"date": "11 เม.ย. 69", "diesel": -4.00, "gasoline": -1.00, "e20": -3.00, "e85": -3.00}, # Big E20/E85 drops
]

# Recalculate sum for verification
# G: 0.6+1+2+6+1+1.2+0.7-1 = 11.5
# E20: 0.6+1+2+6+1+1.2+0.7-0.8-3 = 8.7
# E85: 0.6+1+2+6+1+1.2+0.7-3 = 9.5
# D: 0.5+0.7+1.8+6+1.8+3.5+3.5+2.8-2.2-4 = 14.4

data['trends_th']['table_data'] = new_table

# Update the main history chart for Gasoline to diverge as well
# But for now, fixing trends_th is the priority for that tab.

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Data rebuild with divergence complete.")
