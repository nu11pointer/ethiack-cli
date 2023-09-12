import requests
import sys
from src.static import API_URL, AUTH

def events():
    running = False
    if (len(sys.argv) == 3):
        if (sys.argv[2]) == "running":
            running = True
        else:
            print("Invalid arguments provided!")
            sys.exit()
    r = requests.get(f"{API_URL}/events" + ("?running=True" if running else ""), auth=AUTH)
    if (r.status_code != 200):
        print(f"Request returned {r.status_code}!")
        sys.exit()
    data = r.json()

    if (len(data["events"]) == 0):
        print("There are no events currently running!")
        return
    
    try:
        print("Events")
        print("----------------------------------------")
        for event in data["events"]:
            k = requests.get(f"{API_URL}/events/{event}", auth=AUTH)
            if (k.status_code != 200):
                print(f"Request returned {k.status_code}!")
                sys.exit()
            datak = k.json()
            print(f"  {event}" + " " * (30 - len(event) - 2) + "|" + f"  {datak['name']}")
        print("----------------------------------------")
    except:
        print("You have no events associated!")