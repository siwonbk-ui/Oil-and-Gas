import json
import os

file_path = 'data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Remove the erroneous 13 April entry
table_data = data['trends_th']['table_data']
if table_data and table_data[-1]['date'].startswith('13 เม.ย.'):
    table_data.pop()
    print("Removed 13 Apr entry.")

# We should also fix previous anomalous entries for diesel
# 11 Apr (-4.0), 9 Apr (-2.14), 5 Apr (+2.8), 3 Apr (+3.5), 2 Apr (+3.5), 31 Mar (+1.8), 26 Mar (+6.0)
# Since the actual price of Diesel has been steadily 44.40, these are all artifacts of the bug.
# We will zero them out or remove them if they only contain diesel changes.
for entry in table_data:
    if abs(entry['diesel']) >= 1.0:
        print(f"Zeroing out anomalous diesel change in {entry['date']}: {entry['diesel']}")
        entry['diesel'] = 0.0

# Remove entries that now have all 0s
cleaned_table = []
for entry in table_data:
    if abs(entry['gasoline']) > 0 or abs(entry['e20']) > 0 or abs(entry['e85']) > 0 or abs(entry['diesel']) > 0:
        cleaned_table.append(entry)
    else:
        print(f"Removed fully zeroed entry: {entry['date']}")
        
data['trends_th']['table_data'] = cleaned_table

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
