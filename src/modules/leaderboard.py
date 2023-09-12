import sys
import requests
from math import floor
from src.static import GQL_URL

def leaderboard():
    country = ""
    if (len(sys.argv) == 3):
        if (len(sys.argv[2]) != 2):
            print("Invalid country!")
            return
        country = sys.argv[2]
    query = {
        "operationName": "GetLeaderboard",
        "variables": {
            "limit": 100,
        },
        "query": "query GetLeaderboard($page: Int, $limit: Int, $country: String, $startDate: Date, $endDate: Date, $newcomers: Boolean) {\n  leaderboard(\n    page: $page\n    limit: $limit\n    country: $country\n    newcomers: $newcomers\n    startDate: $startDate\n    endDate: $endDate\n  ) {\n    page\n    total\n    hackers {\n      edges {\n        node {\n          username\n          points\n          globalHackerRank\n          id\n         country\n          pic\n          timeIntervalPoints(startDate: $startDate, endDate: $endDate)\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
    }
    if (country != ""):
        query["variables"]["country"] = country
    p = requests.post(GQL_URL, json=query)
    if (p.status_code != 200):
        print(f"Request returned {p.status_code}!")
        sys.exit()
    gql = p.json()
    total = str(len(gql["data"]["leaderboard"]["hackers"]["edges"]))
    print(f"Leaderboard (TOP {total})")
    print("----------------------------------------")
    rank = "1"
    for hacker in gql["data"]["leaderboard"]["hackers"]["edges"]:
        username = hacker["node"]["username"]
        points = str(floor(hacker["node"]["points"]))
        ctry = hacker["node"]["country"]
        print("  " + rank + ". " + (" " * (int(len(total)) - len(str(rank)))) + "| " + username + " " * (35 - len(username)) + "| " + points + " " * (len(str(floor(gql["data"]["leaderboard"]["hackers"]["edges"][0]["node"]["points"]))) + 1 - len(points)) + "| " + ctry)
        rank = str(int(rank) + 1)
    print("----------------------------------------")