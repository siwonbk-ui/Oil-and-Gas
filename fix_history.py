import json
import os

def fix_history():
    file_path = 'data.json'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Indices to fix: -5, -4, -3, -2 (Apr 05 to Apr 08)
    indices_to_fix = [-5, -4, -3, -2]
    
    modified = False

    for fuel_type in ['gasoline', 'diesel']:
        if fuel_type not in data:
            continue
            
        history = data[fuel_type].get('history', {})
        datasets = history.get('datasets', [])
        
        for dataset in datasets:
            country = dataset.get('label', 'Unknown')
            prices = dataset.get('data', [])
            
            if len(prices) < 10:
                continue
                
            # Good values to anchor the fix
            prev_good = prices[-6] # Apr 04
            curr_good = prices[-1] # Apr 09
            
            # Check if index -5 is significantly lower (>30%) than index -6
            # This indicates the "dip" for that country
            if prices[-5] < (prev_good * 0.7):
                print(f"Fixing {fuel_type} dip for {country}...")
                
                # We'll use a linear interpolation or just carry forward the Apr 04 value
                # Using the stable Apr 04 value is safer as it represents the 'before' state
                for idx in indices_to_fix:
                    # Optional: create a very slight drift so it doesn't look perfectly flat
                    # but for simplicity, carry forward
                    prices[idx] = prev_good
                
                modified = True

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Success: Price history cleaned up and saved to data.json")
    else:
        print("No significant dips found in history (already clean?).")

if __name__ == "__main__":
    fix_history()
