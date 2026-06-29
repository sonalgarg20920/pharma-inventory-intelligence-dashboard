import re
import requests

url = "https://www.1mg.com/drugs/pantosec-d-sr-capsule-141537"

html = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
).text

# Therapeutic Class
therapeutic_match = re.search(
    r'"therapeutic_class":"([^"]+)"',
    html
)

if therapeutic_match:
    print(
        "Therapeutic Class:",
        therapeutic_match.group(1)
    )

# Composition
composition_match = re.search(
    r'Pantosec D SR Capsule alternatives,([^"]+)',
    html
)

if composition_match:
    print(
        "Composition:",
        composition_match.group(1)
    )