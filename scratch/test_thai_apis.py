import urllib.request
import json

def test_thai_apis():
    print("--- Testing chnwt.dev ---")
    try:
        req = urllib.request.Request("https://api.chnwt.dev/thai-oil-api/latest", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('status') == 'success':
                bcp = data['response']['stations'].get('bcp', {})
                date = data['response'].get('date')
                print(f"Date: {date}")
                print(f"Gasohol 95: {bcp.get('gasohol_95', {}).get('price')}")
                print(f"Diesel: {bcp.get('premium_diesel', {}).get('price')}")
                print(f"E20: {bcp.get('gasohol_e20', {}).get('price')}")
            else:
                print("chnwt.dev status not success")
    except Exception as e:
        print(f"chnwt.dev failed: {e}")

    print("\n--- Testing BCP Official v2 ---")
    try:
        req = urllib.request.Request("https://oil-price.bangchak.co.th/ApiOilPrice2/th", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and isinstance(data, list):
                print(f"Date: {data[0].get('CreateDate')}")
                oil_list = json.loads(data[0].get('OilList', '[]'))
                for item in oil_list:
                    name = item.get('OilName', '')
                    price = item.get('PriceToday')
                    print(f"  {name}: {price}")
    except Exception as e:
        print(f"BCP Official failed: {e}")

if __name__ == "__main__":
    test_thai_apis()
