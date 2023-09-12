import sys
import requests
from src.static import GQL_URL

def user():
    if (len(sys.argv) != 3):
        print("Invalid arguments provided!")
        return
    username = sys.argv[2]
    query = {
        "operationName": "GetPublicProfile",
        "variables": {
            "username": username
        },
        "query": "query GetPublicProfile($username: String) {\n  profile(username: $username) {\n    username\n    profile\n    pic\n    country\n    globalHackerRank\n    points\n    created\n    userTypeString\n    __typename\n  }\n}"}
    p = requests.post(GQL_URL, json=query)
    if (p.status_code != 200):
        print(f"Request returned {p.status_code}!")
        sys.exit()
    gql = p.json()
    if (gql["data"]["profile"] is None):
        print(f"User '{username}' not found!")
        sys.exit()

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

    print("User")
    print("----------------------------------------")
    print("Username: " + username)
    print("Rank: #" + rank)
    print("Points: " + str(gql["data"]["profile"]["points"]))
    print("Role: " + gql["data"]["profile"]["userTypeString"])
    print("Joined at: " + gql["data"]["profile"]["created"])
    print("Country: " + (gql["data"]["profile"]["country"] if (gql["data"]["profile"]["country"] is not None) else ""))
    print("URL: https://portal.ethiack.com/" + username)
    print("----------------------------------------")