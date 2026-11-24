import os
import pandas as pd
from pymongo import MongoClient

df = pd.read_csv("SFPL_DataSF_library-usage_Jan_2023 .csv", encoding="utf-8-sig")
df.columns = [str(c).split("\n")[0].strip() for c in df.columns]
print(df.columns.tolist())

for col in ["Provided Email Address", "Within San Francisco County"]:
    df[col] = df[col].map({True: True, False: False, "True": True, "False": False})

df = df.astype(object).where(df.notna(), None)

def num(x):
    return None if x is None else int(x)

def txt(x):
    return None if x is None else str(x)

docs = []
for r in df.to_dict("records"):
    docs.append({
        "patron_type": {"code": num(r["Patron Type Code"]), "definition": txt(r["Patron Type Definition"])},
        "total_checkouts": num(r["Total Checkouts"]),
        "total_renewals": num(r["Total Renewals"]),
        "age_range": txt(r["Age Range"]),
        "home_library": {"code": txt(r["Home Library Code"]), "definition": txt(r["Home Library Definition"])},
        "circulation_active_month": txt(r["Circulation Active Month"]),
        "circulation_active_year": num(r["Circulation Active Year"]),
        "notification": {"code": txt(r["Notification Preference Code"]), "definition": txt(r["Notification Code Definition"])},
        "provided_email_address": r["Provided Email Address"],
        "within_sf_county": r["Within San Francisco County"],
        "year_patron_registered": num(r["Year Patron Registered"]),
    })

client = MongoClient(os.environ["MONGO_URI"])
patrons = client["sfils2026"]["patrons"]
patrons.delete_many({})

BATCH = 1000
for i in range(0, len(docs), BATCH):
    patrons.insert_many(docs[i:i + BATCH], ordered=False)
    if (i // BATCH) % 50 == 0:
        print("inserted", min(i + BATCH, len(docs)), "of", len(docs))

print("Loaded", patrons.count_documents({}), "documents")
client.close()

