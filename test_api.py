import urllib.request
import json
import ssl

def test():
    resource_id = "7d56918d-adbf-42b7-bd36-e4b33d425027"
    url = f"https://catalog.eppo.go.th/api/3/action/datastore_search?resource_id={resource_id}&limit=1000&sort=_id%20desc"
    
    # Bypass SSL verification if needed as Thai gov sites often have cert issues
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print(f"Fetching from: {url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))
            records = data.get('result', {}).get('records', [])
            print(f"Total records fetched: {len(records)}")
            
            if records:
                # Find the record with the most recent date
                latest = records[0]
                print(f"Latest Record according to ID:")
                print(f"  _id: {latest.get('_id')}")
                print(f"  Date: {latest.get('Year')}-{latest.get('Month')}-{latest.get('Date')}")
                print(f"  Item: {latest.get('Item')}")
                print(f"  Country: {latest.get('Country')}")
                print(f"  Price: {latest.get('Price(Baht)')}")

                # Check for any 2026 data
                data_2026 = [r for r in records if str(r.get('Year')) == '2026']
                print(f"\nFound {len(data_2026)} records for 2026")
                if data_2026:
                    print(f"Example 2026 record: {data_2026[0]}")
            else:
                print("No records found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test()
