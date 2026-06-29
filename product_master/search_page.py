import requests



HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "x-city": "Gurgaon",
    "x-platform": "mobileweb-0.0.1",
    "x-1mglabs-platform": "mWeb",
    "x-access-key": "1mg_client_access_key"
}

product = "CIPCAL 500"

url = "https://www.1mg.com/pwa-api/api/v4/search/all"

params = {
    "q": product,
    "filter": "",
    "page_number": 0,
    "scroll_id": "",
    "per_page": 10,
    "types": "sku,allopathy",
    "sort": "relevance",
    "fetch_eta": "true",
    "is_city_serviceable": "true",
    "substitutes_filter": "false"
}

product = "CIPCAL 500"

response = requests.get(
    url,
    params=params,
    headers=HEADERS
)

data = response.json()

for item in data["data"]["search_results"]:

    if "url" in item:
        print(item["url"])