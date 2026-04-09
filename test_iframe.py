import urllib.request
import re

def test():
    url = "https://www.eppo.go.th/graph/main.php?mini=1"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read()
            # Try different encodings
            try:
                html = content.decode('utf-8')
            except:
                html = content.decode('cp874', errors='ignore')
            
            # Print a snippet to verify
            print(f"HTML Length: {len(html)}")
            
            # Search for Singapore price to verify
            # In the screenshot it was 112.48 for Diesel
            match = re.search(r'สิงคโปร์.*?([0-9.]+)', html, re.DOTALL)
            if match:
                print(f"Found price for Singapore: {match.group(1)}")
            
            # Check for date
            date_match = re.search(r'(\d+)\s+([ก-ฮ.]+)\s+(\d{4}|\d{2})', html)
            if date_match:
                print(f"Date found: {date_match.group(0)}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test()
