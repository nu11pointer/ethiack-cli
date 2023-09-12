import sys
import requests
from src.static import API_URL, AUTH

def event():
    if (len(sys.argv) != 3):
        print("Invalid arguments provided!")
        return
    event = sys.argv[2]

    r = requests.get(f"{API_URL}/events/{event}", auth=AUTH)
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