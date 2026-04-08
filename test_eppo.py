import urllib.request
import re
import json

def fetch_eppo_prices():
    """Scrapes ASEAN oil prices from EPPO iframe source"""
    url = "https://www.eppo.go.th/graph/main.php?mini=1"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
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

if __name__ == "__main__":
    result = fetch_eppo_prices()
    print("\nFinal Result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
