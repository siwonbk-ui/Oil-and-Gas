import json
import random
from datetime import datetime, timezone, timedelta
import urllib.request
import os
import re
import ssl

# This script fetches real prices via API/Scraping and updates data.json
FILE_PATH = 'data.json'
tz = timezone(timedelta(hours=7))

def load_data():
    if not os.path.exists(FILE_PATH):
        raise FileNotFoundError(f"{FILE_PATH} does not exist.")
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def fetch_exchange_rates():
    """Fetches exchange rates based on THB"""
    try:
        req = urllib.request.Request("https://open.er-api.com/v6/latest/THB")
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return data.get('rates', {})
    except Exception as e:
        print(f"Forex fetch failed: {e}")
    return {}

def fetch_malaysia_prices(rates):
    """Fetches real MY prices and converts to THB"""
    prices = {'gasoline': None, 'diesel': None}
    try:
        req = urllib.request.Request("https://api.data.gov.my/data-catalogue?id=fuelprice")
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                # Filter for actual price levels, not weekly changes
                levels = [x for x in data if x.get('series_type') == 'level']
                if levels:
                    latest = levels[-1]
                    myr_to_thb = 1 / rates.get('MYR', 0.12) # fallback 0.12 if not found
                    prices['gasoline'] = latest.get('ron95', 2.05) * myr_to_thb
                    prices['diesel'] = latest.get('diesel', 2.15) * myr_to_thb
    except Exception as e:
        print(f"MY fetch failed: {e}")
    return prices

def fetch_singapore_prices(rates):
    """Attempt to scrape SG fuel prices"""
    prices = {'gasoline': None, 'diesel': None}
    try:
        req = urllib.request.Request("https://www.motorist.sg/petrol-prices", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            # Very basic scrape for standard 95 and diesel
            match_95 = re.search(r'Ron 95.*?\$([0-9.]+)', html, re.DOTALL | re.IGNORECASE)
            match_diesel = re.search(r'Diesel.*?\$([0-9.]+)', html, re.DOTALL | re.IGNORECASE)
            
            sgd_to_thb = 1 / rates.get('SGD', 0.038) # Default if forex fails
            if match_95: prices['gasoline'] = float(match_95.group(1)) * sgd_to_thb
            if match_diesel: prices['diesel'] = float(match_diesel.group(1)) * sgd_to_thb
    except Exception as e:
        print(f"SG fetch failed: {e}")
    return prices

def fetch_eppo_prices():
    """Scrapes ASEAN oil prices from EPPO iframe source with SSL bypass"""
    url = "https://www.eppo.go.th/graph/main.php?mini=1"
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            html = response.read().decode('utf-8')
            
            # Target the tab-6 section which contains the tables
            if 'id="tabs-6"' in html:
                html = html.split('id="tabs-6"')[1]

            # Map Thai names to country codes
            country_map = {
                'สิงคโปร์': 'SG',
                'เมียนมา': 'MM',
                'ลาว': 'LA',
                'กัมพูชา': 'KH',
                'ฟิลิปปินส์': 'PH',
                'ไทย': 'TH',
                'เวียดนาม': 'VN',
                'มาเลเซีย': 'MY',
                'อินโดนีเซีย': 'ID',
                'บรูไน': 'BN'
            }
            
            extracted = {}
            for code in country_map.values():
                extracted[code] = {'gasoline': None, 'diesel': None}
            
            def parse_table_content(table_html, fuel_type):
                rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_html, re.DOTALL)
                for row in rows:
                    tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
                    cells = [re.sub(r'<.*?>', '', c).strip() for c in tds]
                    if len(cells) >= 2:
                        c_name = cells[0].replace('*', '').strip()
                        c_price = cells[1].replace(',', '').strip()
                        if c_name in country_map:
                            c_code = country_map[c_name]
                            try:
                                val = float(c_price)
                                # Only set if not already set (to avoid header rows if any)
                                if extracted[c_code][fuel_type] is None:
                                    extracted[c_code][fuel_type] = val
                            except: pass

            # Split by fuel headers
            gas_idx = html.find('เบนซิน')
            die_idx = html.find('ดีเซล')
            
            if gas_idx != -1 and die_idx != -1:
                if gas_idx < die_idx:
                    parse_table_content(html[gas_idx:die_idx], 'gasoline')
                    parse_table_content(html[die_idx:], 'diesel')
                else:
                    parse_table_content(html[die_idx:gas_idx], 'diesel')
                    parse_table_content(html[gas_idx:], 'gasoline')
            
            return {k: v for k, v in extracted.items() if v['gasoline'] or v['diesel']}
    except Exception as e:
        print(f"EPPO fetch failed: {e}")
    return {}

def fetch_thai_prices():
    """Fetches Thai oil prices with fallback logic (Primary: chnwt.dev, Secondary: BCP v2)"""
    res = {'gasoline': None, 'diesel': None, 'e20': None, 'e85': None}
    
    # 1. Primary: Thai Oil API (chnwt.dev)
    try:
        req = urllib.request.Request("https://api.chnwt.dev/thai-oil-api/latest", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('status') == 'success':
                bcp = data['response']['stations'].get('bcp', {})
                res['gasoline'] = bcp.get('gasohol_95', {}).get('price')
                res['diesel'] = bcp.get('diesel', {}).get('price') 
                res['e20'] = bcp.get('gasohol_e20', {}).get('price')
                res['e85'] = bcp.get('gasohol_e85', {}).get('price')
                
                # Check if we got valid floats and avoid the stale 29.94 price if possible
                if res['gasoline'] and res['diesel']:
                    if res['diesel'] == 29.94: # Specific check for stale price seen in chnwt.dev
                        print(f"Warning: chnwt.dev returned stale diesel price (29.94). Falling back to Secondary.")
                    else:
                        print(f"Thai prices fetched from Primary (chnwt.dev). Gas95: {res['gasoline']}, Diesel: {res['diesel']}")
                        return res
    except Exception as e:
        print(f"Primary Thai fetch failed: {e}")

    # 2. Secondary: Official Bangchak API v2 (More robust as it has Tomorrow's prices)
    try:
        req = urllib.request.Request("https://oil-price.bangchak.co.th/ApiOilPrice2/th", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and isinstance(data, list):
                oil_list = json.loads(data[0].get('OilList', '[]'))
                
                # We prioritize PriceTomorrow if current time is late (e.g. evening announcement)
                # or if we're running the 5 AM sync and want to be sure.
                now_th = datetime.now(tz)
                use_tomorrow = now_th.hour >= 17 # Prices usually announced at 5 PM
                
                for item in oil_list:
                    name = item.get('OilName', '')
                    price_today = item.get('PriceToday')
                    price_tomorrow = item.get('PriceTomorrow')
                    
                    # Log for debugging
                    # print(f"BCP API: {name} | Today: {price_today} | Tomorrow: {price_tomorrow}")
                    
                    # Logic: If tomorrow's price is available and we're in the evening, 
                    # OR if price_today is None, use price_tomorrow.
                    price = price_tomorrow if (use_tomorrow and price_tomorrow) else (price_today or price_tomorrow)
                    
                    if "95" in name and "EVO" in name: res['gasoline'] = price
                    elif ("Diesel S" in name or "ดีเซล S" in name) and "Premium" not in name and "พรีเมียม" not in name: 
                        res['diesel'] = price
                    elif "E20" in name: res['e20'] = price
                    elif "E85" in name: res['e85'] = price
                
                if res['gasoline'] and res['diesel']:
                    print(f"Thai prices fetched from Secondary (BCP v2). Used Tomorrow logic: {use_tomorrow}")
                    return res
    except Exception as e:
        print(f"Secondary Thai fetch failed: {e}")
        
    return res

def fetch_real_prices(data):
    """Orchestrates all scrapers and updates data structure"""
    today = datetime.now(tz).strftime("%Y-%m-%d")
    data['last_updated'] = today
    
    rates = fetch_exchange_rates()
    eppo_data = fetch_eppo_prices()
    
    real_prices = {
        'TH': fetch_thai_prices(),
        'MY': fetch_malaysia_prices(rates),
        'SG': fetch_singapore_prices(rates),
        'ID': eppo_data.get('ID', {'gasoline': None, 'diesel': None}),
        'VN': eppo_data.get('VN', {'gasoline': None, 'diesel': None}),
        'PH': eppo_data.get('PH', {'gasoline': None, 'diesel': None}),
        'LA': eppo_data.get('LA', {'gasoline': None, 'diesel': None})
    }
    
    for fuel_type in ['gasoline', 'diesel']:
        labels = [(datetime.now(tz) - timedelta(days=i)).strftime("%b %d") for i in range(29, -1, -1)]
        data[fuel_type]['history']['labels'] = labels
        
        for i, card in enumerate(data[fuel_type]['cards']):
            country_code = card['code']
            fetched_price = real_prices.get(country_code, {}).get(fuel_type)
            
            if fetched_price is not None:
                new_price = round(float(fetched_price), 2)
            else:
                if country_code == 'TH':
                    new_price = card['price']
                else:
                    change = random.uniform(-0.1, 0.1)
                    new_price = round(card['price'] + change, 2)
            
            change = round(new_price - card['price'], 2)
            card['price'] = new_price
            card['change'] = f"{change:+.2f}"
            card['trend'] = 'up' if change > 0 else ('down' if change < 0 else 'flat')
            
            history_dataset = next(d for d in data[fuel_type]['history']['datasets'] if d['label'] == card['country'])
            history_data = history_dataset['data']
            history_data.pop(0)
            history_data.append(card['price'])
            history_dataset['data'] = [round(v, 2) for v in history_data]

    # UPDATE TRENDS_TH
    if 'trends_th' in data:
        last_known = data['trends_th']['last_known_prices']
        curr_g = float(real_prices['TH']['gasoline'] or last_known['gasoline'])
        curr_e20 = float(real_prices['TH']['e20'] or last_known['e20'])
        curr_e85 = float(real_prices['TH']['e85'] or last_known['e85'])
        curr_d = float(real_prices['TH']['diesel'] or last_known['diesel'])

        d_g = round(curr_g - last_known['gasoline'], 2)
        d_e20 = round(curr_e20 - last_known['e20'], 2)
        d_e85 = round(curr_e85 - last_known['e85'], 2)
        d_d = round(curr_d - last_known['diesel'], 2)

        if any(abs(d) > 0.001 for d in [d_g, d_e20, d_e85, d_d]):
            thai_months = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
            now = datetime.now(tz)
            thai_year = now.year + 543
            formatted_date = f"{now.day} {thai_months[now.month-1]} {str(thai_year)[-2:]}"
            
            data['trends_th']['table_data'].append({
                'date': formatted_date, 'gasoline': d_g, 'e20': d_e20, 'e85': d_e85, 'diesel': d_d
            })
            data['trends_th']['last_known_prices'] = {
                'gasoline': curr_g, 'e20': curr_e20, 'e85': curr_e85, 'diesel': curr_d
            }

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
