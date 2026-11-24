import os
import pprint
from pymongo import MongoClient

client = MongoClient(os.environ["MONGO_URI"])
patrons = client["sfils2026"]["patrons"]

def repeat_patrons():
    total = patrons.count_documents({})
    repeat = patrons.count_documents({"total_checkouts": {"$gt": 1}})
    return{ "total_patrons": total,
            "repeat_patrons": repeat,
            "repeat_pct": round(100 * repeat / total, 1)
    }

def renewals():
    total = patrons.count_documents({})
    renewed = patrons.count_documents({"total_renewals": {"$gt": 0}})
    result = list(patrons.aggregate([
        {"$group": {"_id": None, "total_renewals": {"$sum": "$total_renewals"}}}
    ]))
    return {"patrons_who_renewed": renewed,
            "total_renewals": result[0]["total_renewals"],
            "renewed_pct": round(100 * renewed / total, 1)
            }

def most_active_patron():
    top = patrons.find_one(sort=[("total_checkouts", -1)])
    return list(patrons.find({"total_checkouts": top["total_checkouts"]}, {"_id": 0}))

if __name__ == "__main__":
    pprint.pprint(repeat_patrons())
    pprint.pprint(renewals())
    pprint.pprint(most_active_patron())

