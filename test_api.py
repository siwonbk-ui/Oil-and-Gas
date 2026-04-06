import urllib.request
import json
import re

def test_malaysia():
    print("\n--- MALAYSIA API ---")
    try:
        url = "https://api.data.gov.my/data-catalogue?id=fuelprice&limit=1"
        # The API doesn't support generic limit=1&sort=-date usually, so let's fetch all and get last or try sorting
        req = urllib.request.Request("https://api.data.gov.my/data-catalogue?id=fuelprice")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print("Total MY records:", len(data))
            print("Latest:", data[-1])
    except Exception as e:
        print(f"MY Error: {e}")

def test_singapore():
    print("\n--- SINGAPORE (MOTORIST) ---")
    try:
        req = urllib.request.Request("https://www.motorist.sg/petrol-prices", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            # Look for SPC 95 and Diesel. SPC is col index, row is fuel type
            # Too complex to parse without BS4, we can mock or do simple regex
            match_95 = re.search(r'Ron 95.*?\$([0-9.]+)', html, re.DOTALL | re.IGNORECASE)
            match_diesel = re.search(r'Diesel.*?\$([0-9.]+)', html, re.DOTALL | re.IGNORECASE)
            if match_95: print("SG 95:", match_95.group(1))
            if match_diesel: print("SG Diesel:", match_diesel.group(1))
    except Exception as e:
        print(f"SG Error: {e}")

if __name__ == "__main__":
    test_malaysia()
    test_singapore()
