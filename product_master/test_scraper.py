import requests

url = "https://www.1mg.com/drugs/pantosec-d-sr-capsule-141537"

html = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
).text

for keyword in [
    "Pantoprazole",
    "Domperidone",
    "GASTRO"
]:

    pos = html.find(keyword)

    print("\n")
    print("=" * 50)
    print(keyword)
    print("=" * 50)

    print(
        html[
            max(0, pos - 500):
            pos + 500
        ]
    )