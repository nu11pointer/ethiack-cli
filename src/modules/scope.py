import sys
import requests
from src.static import API_URL, AUTH

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

    r = requests.get(f"{API_URL}/events/{event}/scope", auth=AUTH)
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