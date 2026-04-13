import urllib.request
import json

def test():
    print("--- Bangchak API ---")
    try:
        req = urllib.request.Request("https://oil-price.bangchak.co.th/ApiOilPrice2/th", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and isinstance(data, list):
                oil_list = json.loads(data[0].get('OilList', '[]'))
                for item in oil_list:
                    print(f"{item.get('OilName')}: {item.get('PriceToday')} (Tomorrow: {item.get('PriceTomorrow')})")
    except Exception as e:
        print(f"BCP failed: {e}")

    print("\n--- Thai Oil API (chnwt.dev) ---")
    try:
        req = urllib.request.Request("https://api.chnwt.dev/thai-oil-api/latest", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('status') == 'success':
                stations = data['response']['stations']
                for station, prices in stations.items():
                    print(f"Station: {station}")
                    for oil, pinfo in prices.items():
                        print(f"  {oil}: {pinfo.get('price')}")
    except Exception as e:
        print(f"chnwt failed: {e}")

if __name__ == '__main__':
    test()
