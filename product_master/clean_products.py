import re
import pandas as pd

df = pd.read_csv(
    "top_521_products.csv"
)



def clean_product_name(name):

    name = str(name).upper()

    patterns = [
        r"\(\d+\)",
        r"\d+'TAB",
        r"\d+'T",
        r"\d+'C",
        r"\d+ML",
        r"\bTABLET\b",
        r"\bTAB\b",
        r"\bCAPSULE\b",
        r"\bCAPS\b",
        r"\bCAP\b",
        r"\bSYRUP\b",
        r"\bSYP\b",
        r"\bSUSP\b",
        r"\bMG\b"
    ]

    for p in patterns:
        name = re.sub(p, "", name)

    name = re.sub(
        r"[^\w\s\-]",
        "",
        name
    )

    name = re.sub(
        r"\s+",
        " ",
        name
    )

    return name.strip()

df["clean_name"] = (
    df["product_name"]
    .apply(clean_product_name)
)

print(
    df[
        [
            "product_name",
            "clean_name"
        ]
    ].head(20)
)

df.to_csv(
    "top_521_cleaned.csv",
    index=False
)