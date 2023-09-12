import requests
import sys
from src.static import API_URL, GQL_URL, AUTH

def profile():
    r = requests.get(f"{API_URL}/me", auth=AUTH)
    if (r.status_code != 200):
        print(f"Request returned {r.status_code}!")
        sys.exit()
    data = r.json()
    query = {
        "operationName": "GetPublicProfile",
        "variables": {
            "username": data["username"]
        },
        "query": "query GetPublicProfile($username: String) {\n  profile(username: $username) {\n    username\n    profile\n    pic\n    country\n    globalHackerRank\n    points\n    created\n    userTypeString\n    __typename\n  }\n}"}
    p = requests.post(GQL_URL, json=query)
    if (p.status_code != 200):
        print(f"Request returned {p.status_code}!")
        sys.exit()
    gql = p.json()
    rank = "0"
    if (gql["data"]["profile"]["globalHackerRank"] == 0):
        rank = "Unranked"
    elif (gql["data"]["profile"]["globalHackerRank"] == 1):
        rank = "1 (TOP 1)"
    elif (gql["data"]["profile"]["globalHackerRank"] <= 3):
        rank = str(gql["data"]["profile"]["globalHackerRank"]) + " (TOP 3)"
    elif (gql["data"]["profile"]["globalHackerRank"] <= 10):
        rank = str(gql["data"]["profile"]["globalHackerRank"]) + " (TOP 10)"
    else:
        rank = str(gql["data"]["profile"]["globalHackerRank"])

    print("Profile")
    print("----------------------------------------")
    print("Username: " + data["username"])
    print("Name: " + data["name"])
    print("Rank: #" + rank)
    print("Points: " + str(gql["data"]["profile"]["points"]))
    print("Role: " + gql["data"]["profile"]["userTypeString"])
    print("Joined at: " + gql["data"]["profile"]["created"])
    print("Country: " + data["country"] if ("country" in data and data["country"] is not None) else "")
    print("URL: https://portal.ethiack.com/" + data["username"])
    print("----------------------------------------")