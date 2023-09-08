#!/usr/bin/env python3

import requests
import os
import sys
from math import floor
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

__version__ = "1.0.0"

load_dotenv()
KEY = os.getenv("ETHIACK_API_KEY")
SECRET = os.getenv("ETHIACK_API_SECRET")
auth = HTTPBasicAuth(KEY, SECRET)

def help():
    print("""Modules:
    event <event>               Get information regarding a specific event
    events [running]            Gets a list of events you're associated with
    help                        Show the help page
    leaderboard [country]       Hacker leaderboard
    profile                     Your public profile
    scope <event> [save]        Get the scope for an event
    user <user>                 Get a user's public profile
    version                     Show the utility version""")

def event():
    if (len(sys.argv) != 3):
        print("Invalid arguments provided!")
        return
    event = sys.argv[2]

    r = requests.get(f"https://api.ethiack.com/v1/events/{event}", auth=auth)
    if (r.status_code == 404):
        print(f"Event not found!")
        sys.exit()
    elif (r.status_code != 200):
        print(f"Request returned {r.status_code}!")
        sys.exit()
    data = r.json()

    match data["status"]:
        case 5:
            status = "Retesting"
        case 3:
            status = "Running"
        case 6:
            status = "Finished"
        case _:
            status = "Unknown"

    print("Event")
    print("----------------------------------------")
    print("ID: " + str(data["id"]))
    print("Slug: " + event)
    print("Name: " + data["name"])
    print("Dimension: " + data["dimension"])
    print("Category: " + data["event_category"])
    print("Type: " + data["event_type"])
    print("Start: " + data["start_date"])
    print("End: " + data["end_date"])
    print("Latitude: " + ("" if data["latitude"] is None else str(data["latitude"])))
    print("Longitude: " + ("" if data["longitude"] is None else str(data["longitude"])))
    print("Status: " + status)
    print("----------------------------------------")

def events():
    running = False
    if (len(sys.argv) == 3):
        if (sys.argv[2]) == "running":
            running = True
        else:
            print("Invalid arguments provided!")
            sys.exit()
    r = requests.get("https://api.ethiack.com/v1/events" + ("?running=True" if running else ""), auth=auth)
    if (r.status_code != 200):
        print(f"Request returned {r.status_code}!")
        sys.exit()
    data = r.json()

    if (len(data["events"]) == 0):
        print("There's no running events, currently!")
        return
    
    try:
        print("Events")
        print("----------------------------------------")
        for event in data["events"]:
            k = requests.get(f"https://api.ethiack.com/v1/events/{event}", auth=auth)
            if (k.status_code != 200):
                print(f"Request returned {k.status_code}!")
                sys.exit()
            datak = k.json()
            print(f"  {event}" + " " * (30 - len(event) - 2) + "|" + f"  {datak['name']}")
        print("----------------------------------------")
    except:
        print("You have no events!")

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
    p = requests.post("https://gql.ethiack.com/graphql", json=query)
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

def profile():
    r = requests.get("https://api.ethiack.com/v1/me", auth=auth)
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
    p = requests.post("https://gql.ethiack.com/graphql", json=query)
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
    print("VAT: " + gql["data"]["profile"]["profile"]["vat"])
    print("Role: " + gql["data"]["profile"]["userTypeString"])
    print("Entity: " + gql["data"]["profile"]["profile"]["entity_type"])
    print("Joined at: " + gql["data"]["profile"]["created"])
    print("Country: " + data["country"] if ("country" in data and data["country"] is not None) else "")
    print("URL: https://portal.ethiack.com/" + data["username"])
    print("----------------------------------------")

def scope():
    save = False
    idomains = []
    odomains = []
    if (len(sys.argv) == 3):
        event = sys.argv[2]
    elif (len(sys.argv) == 4):
        event = sys.argv[2]
        if (sys.argv[3] == "save"):
            save = True
        else:
            print("Invalid arguments provided!")
            return
    else:
        print("Invalid arguments provided!")
        return

    r = requests.get(f"https://api.ethiack.com/v1/events/{event}/scope", auth=auth)
    if (r.status_code == 404):
        print(f"Event not found!")
        sys.exit()
    elif (r.status_code != 200):
        print(f"Request returned {r.status_code}!")
        sys.exit()
    data = r.json()
    print(f"Scope ({event})")
    print("----------------------------------------")
    print("  In-Scope")
    print("  --------------------------------------")
    for ins in data["in_scope"]["assets"]:
        if (ins["type"] == "domain"):
            idomains.append(ins["value"])
        print(f"    " + ins["value"] + " " * (60 - len(ins["value"])) + "| " + ins["type"] + ((" | " + ins["description"]) if ins["description"] is not None and len(ins["description"]) > 0 else ""))
    print()
    print("  Out-of-Scope")
    print("  --------------------------------------")
    for outs in data["out_of_scope"]["assets"]:
        if (outs["type"] == "domain"):
            odomains.append(outs["value"])
        print(f"    " + outs["value"] + " " * (60 - len(outs["value"])) + "| " + outs["type"] + ((" | " + outs["description"]) if ins["description"] is not None and len(outs["description"]) > 0 else ""))
    if (save):
        print()
        with open("inscope.txt", "w") as fp:
            fp.writelines("\n".join(sorted(idomains)))
            print("File 'inscope.txt' saved!")
        with open("outofscope.txt", "w") as fp:
            fp.writelines("\n".join(sorted(odomains)))
            print("File 'outofscope.txt' saved!")

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
    p = requests.post("https://gql.ethiack.com/graphql", json=query)
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
    print("Entity: " + (gql["data"]["profile"]["profile"]["entity_type"] if ("entity_type" in gql["data"]["profile"]["profile"]) else ""))
    print("Joined at: " + gql["data"]["profile"]["created"])
    print("Country: " + (gql["data"]["profile"]["country"] if (gql["data"]["profile"]["country"] is not None) else ""))
    print("URL: https://portal.ethiack.com/" + username)
    print("----------------------------------------")

def version():
    print("ethiack-cli v" + __version__)

def main():
    print()
    if KEY is None:
        print("Environment variable ETHIACK_API_KEY is not set!")
        sys.exit()
    if SECRET is None:
        print("Environment variable ETHIACK_API_SECRET is not set!")
        sys.exit()
    
    if (len(sys.argv) < 2):
        print("No argument provided!\n")
        print(f"Usage: {__file__} help")
        sys.exit()
    
    match sys.argv[1]:
        case "event":
            event()
        case "events":
            events()
        case "help":
            help()
        case "leaderboard":
            leaderboard()
        case "profile":
            profile()
        case "scope":
            scope()
        case "user":
            user()
        case "version":
            version()
        case _:
            print(f"Invalid module '{sys.argv[1]}'")
            sys.exit()
    
if __name__ == "__main__":
    main()