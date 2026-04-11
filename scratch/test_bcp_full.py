import urllib.request
import json

def test_bcp_full():
    url = "https://oil-price.bangchak.co.th/ApiOilPrice2/th"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and isinstance(data, list):
                oil_list = json.loads(data[0].get('OilList', '[]'))
                for item in oil_list:
                    print(f"Name: {item.get('OilName')}")
                    print(f"  PriceToday: {item.get('PriceToday')}")
                    print(f"  PriceTomorrow: {item.get('PriceTomorrow')}")
                    print(f"  Unit: {item.get('Unit')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_bcp_full()
