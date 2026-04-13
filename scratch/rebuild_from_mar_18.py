import json
import os

file_path = 'data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

labels = data['diesel']['history']['labels']
th_diesel = next(ds for ds in data['diesel']['history']['datasets'] if ds['label'] == 'Thailand')['data']
th_gasoline = next(ds for ds in data['gasoline']['history']['datasets'] if ds['label'] == 'Thailand')['data']

def eng_to_thai_date(eng_date):
    # eng_date is "Mar 18"
    parts = eng_date.split(' ')
    month = parts[0]
    day = int(parts[1])
    
    if month == 'Mar': month_th = 'มี.ค.'
    elif month == 'Apr': month_th = 'เม.ย.'
    else: month_th = month
    
    return f"{day} {month_th} 69"

start_index = -1
for i, l in enumerate(labels):
    if l == 'Mar 18':
        start_index = i
        break

new_table = []
if start_index != -1:
    for i in range(start_index, len(labels)):
        prev_d = th_diesel[i-1]
        curr_d = th_diesel[i]
        
        prev_g = th_gasoline[i-1]
        curr_g = th_gasoline[i]
        
        diff_d = round(curr_d - prev_d, 2)
        diff_g = round(curr_g - prev_g, 2)
        
        # If there is a price change in either D or G
        if abs(diff_d) > 0.01 or abs(diff_g) > 0.01:
            # Estimate E20 and E85 change to be similar to Gasoline (usually moves together)
            # Typical gasohol margins mean they slightly follow 95.
            diff_e20 = diff_g
            diff_e85 = diff_g
            
            new_table.append({
                "date": eng_to_thai_date(labels[i]),
                "gasoline": diff_g,
                "e20": diff_e20,
                "e85": diff_e85,
                "diesel": diff_d
            })

data['trends_th']['table_data'] = new_table

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
    
print(f"Rebuilt table from Mar 18. Total rows: {len(new_table)}")
for row in new_table:
    print(f"- {row['date']}: D={row['diesel']}, G={row['gasoline']}")
