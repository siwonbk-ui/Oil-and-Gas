import urllib.request
import re

def test():
    url = "https://www.eppo.go.th/graph/main.php?mini=1"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read()
            html = content.decode('cp874', errors='ignore')
            
            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL)
            for row in rows:
                tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
                clean_tds = [re.sub(r'<.*?>', '', td).replace('*', '').strip() for td in tds]
                if len(clean_tds) == 2:
                    print(f"Name: {repr(clean_tds[0])}, Price: {clean_tds[1]}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test()
