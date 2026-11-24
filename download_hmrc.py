import requests
import pandas as pd

# HMRC overseas trade API: UK imports of crude oil (2709) and refined oils (2710)
url = "https://api.uktradeinfo.com/OTS"
query = (
    "?$filter=MonthId ge 201901"
    " and (FlowTypeId eq 1 or FlowTypeId eq 3)"
    " and CommodityId ge 27090000 and CommodityId le 27109999"
)

rows = []
next_url = url + query
while next_url:
    response = requests.get(next_url, timeout=60)
    response.raise_for_status()
    data = response.json()
    rows.extend(data["value"])
    next_url = data.get("@odata.nextLink")
    print(f"Downloaded {len(rows)} rows so far...")

df = pd.DataFrame(rows)
df.to_csv("hmrc_oil_imports.csv", index=False)
print(f"Done: {len(df)} rows saved to hmrc_oil_imports.csv")