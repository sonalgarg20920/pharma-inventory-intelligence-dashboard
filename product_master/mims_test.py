import requests
import pandas as pd
import time


def search_netmeds(product_name):

    url = "https://www.netmeds.com/ext/search/application/api/v1.0/products"

    params = {
        "page_id": "*",
        "page_size": 5,
        "q": product_name
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        items = data.get("items", [])

        results = []

        for item in items:

            attrs = item.get(
                "attributes",
                {}
            )

            results.append({
                "matched_product": attrs.get(
                    "mstar-displaynamewops"
                ),
                "generic_name": attrs.get(
                    "genericname"
                ),
                "therapeutic_class": attrs.get(
                    "categorynamelevel1"
                ),
                "sub_class": attrs.get(
                    "categorynamelevel3"
                ),
                "manufacturer": attrs.get(
                    "marketername"
                )
            })

        return results

    except Exception as e:

        print(
            f"Error for {product_name}: {e}"
        )

        return []


# Load master file
master_df = pd.read_csv(
    "product_master_test.csv"
)

# Get score=0 products
unmatched_df = master_df[
    master_df["score"] == 0
]

products = (
    unmatched_df["product_name"]
    .dropna()
    .unique()
    .tolist()
)

print(
    "Products to retry:",
    len(products)
)

results = []

for product in products:

    print(
        f"Processing: {product}"
    )

    matches = search_netmeds(
        product
    )

    if len(matches) == 0:

        results.append({
            "inventory_product": product,
            "rank": 0,
            "matched_product": None,
            "generic_name": None,
            "therapeutic_class": None,
            "sub_class": None,
            "manufacturer": None
        })

    else:

        for idx, match in enumerate(matches):

            results.append({
                "inventory_product": product,
                "rank": idx + 1,
                "matched_product": match["matched_product"],
                "generic_name": match["generic_name"],
                "therapeutic_class": match["therapeutic_class"],
                "sub_class": match["sub_class"],
                "manufacturer": match["manufacturer"]
            })

    time.sleep(1)

# Save
netmeds_df = pd.DataFrame(
    results
)

netmeds_df.to_csv(
    "netmeds_review.csv",
    index=False
)

print(
    "\nSaved:",
    len(netmeds_df),
    "rows"
)