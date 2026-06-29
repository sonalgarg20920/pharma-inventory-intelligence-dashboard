import requests
import pandas as pd
import time
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "x-city": "Gurgaon",
    "x-platform": "mobileweb-0.0.1",
    "x-1mglabs-platform": "mWeb",
    "x-access-key": "1mg_client_access_key"
}


def normalize(text):

    text = str(text).upper()

    text = re.sub(
        r'[^A-Z0-9]',
        '',
        text
    )

    return text


def search_1mg(product_name):

    url = "https://www.1mg.com/pwa-api/api/v4/search/all"

    params = {
        "q": product_name,
        "filter": "",
        "page_number": 0,
        "scroll_id": "",
        "per_page": 15,
        "types": "sku,allopathy",
        "sort": "relevance",
        "fetch_eta": "true",
        "is_city_serviceable": "true",
        "substitutes_filter": "false"
    }

    for attempt in range(3):

        try:

            response = requests.get(
                url,
                params=params,
                headers=HEADERS,
                timeout=20
            )

            data = response.json()

            if "data" not in data:
                return None

            break

        except Exception as e:

            print(f"Retry {attempt + 1}: {e}")

            time.sleep(5)

    else:

        return None

    results = (
        data
        .get("data", {})
        .get("search_results", [])
    )

    best_match = None
    best_score = -999

    normalized_product = normalize(
        product_name
    )

    product_words = [
        w.upper()
        for w in str(product_name).split()
    ]

    for item in results:

        if (
            "name" not in item
            or "url" not in item
        ):
            continue

        matched_name = item["name"]

        normalized_match = normalize(
            matched_name
        )

        score = 0

        # Strong exact match bonus
        if normalized_product in normalized_match:
            score += 10

        # Word matching
        for word in product_words:

            if word in matched_name.upper():
                score += 1

        # Exact numeric matching
        numbers_in_match = re.findall(
            r"\d+",
            matched_name
        )

        for word in product_words:

            if word.isdigit():

                if word in numbers_in_match:
                    score += 10

                

        if score > best_score:

            best_score = score

            product_type = (
                "OTC"
                if "/otc/" in item["url"]
                else "DRUG"
            )

            best_match = {
                "name": matched_name,
                "url": (
                    "https://www.1mg.com"
                    + item["url"]
                ),
                "type": product_type,
                "score": score
            }

    return best_match


def get_drug_details(drug_url):

    try:

        html = requests.get(
            drug_url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        ).text

        therapeutic_match = re.search(
            r'"therapeutic_class":"([^"]+)"',
            html
        )

        composition_match = re.search(
            r'alternatives,([^"]+)',
            html
        )

        therapeutic_class = (
            therapeutic_match.group(1)
            if therapeutic_match
            else None
        )

        composition = (
            composition_match.group(1).strip()
            if composition_match
            else None
        )

        return {
            "composition": composition,
            "therapeutic_class": therapeutic_class
        }

    except Exception:

        return {
            "composition": None,
            "therapeutic_class": None
        }


# =====================================
# TEST ON FIRST 20 PRODUCTS
# =====================================

df_products = pd.read_csv(
    "top_521_cleaned.csv"
)

master_df = pd.read_csv(
    "product_master_test.csv"
)
unmatched_df = master_df[
    master_df["score"] == 0
]

products = (
    unmatched_df["product_name"]
    .dropna()
    .unique()
    .tolist()
)


results = []

for product in products:

    print(f"Processing: {product}")

    result = search_1mg(product)

    if result is None:

        results.append({
            "product_name": product,
            "matched_name": None,
            "product_type": None,
            "url": None,
            "composition": None,
            "therapeutic_class": None,
            "score": 0
        })

        continue

    if result["type"] == "DRUG":

        details = get_drug_details(
            result["url"]
        )

        composition = details["composition"]
        therapeutic_class = details["therapeutic_class"]

    else:

        composition = None
        therapeutic_class = "OTC"

    results.append({

        "product_name": product,
        "matched_name": result["name"],
        "product_type": result["type"],
        "url": result["url"],
        "composition": composition,
        "therapeutic_class": therapeutic_class,
        "score": result["score"]

    })

    time.sleep(1)

master_df = pd.DataFrame(results)

master_df.to_csv(
    "product_master_test.csv",
    index=False
)

print(master_df)
print("Rows:", len(master_df))