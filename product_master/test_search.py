from ddgs import DDGS

results = list(
    DDGS().text(
        "PANTOSEC DSR 1mg",
        max_results=10
    )
)

print(results)