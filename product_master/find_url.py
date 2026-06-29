import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

query = "PANTOSEC DSR"

search_url = (
    "https://html.duckduckgo.com/html/?q="
    + query.replace(" ", "+")
    + "+site:1mg.com/drugs"
)

print("Searching:", query)

response = requests.get(
    search_url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

html = response.text

print("Status:", response.status_code)


def get_1mg_url(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    for a in soup.find_all(
        "a",
        href=True
    ):

        href = a["href"]

        if "uddg=" in href:

            try:

                real_url = unquote(
                    href.split("uddg=")[1]
                    .split("&")[0]
                )

                if (
                    "1mg.com/drugs"
                    in real_url
                ):

                    return real_url

            except Exception:
                pass
    print("\nNo URL found")
    print("First 10 hrefs:")

    for a in soup.find_all("a", href=True)[:10]:
        print(a["href"])
    return None


drug_url = get_1mg_url(html)

print("\nDrug URL:")
print(drug_url)