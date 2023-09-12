#!/usr/bin/env python3

import sys
from src.modules.event import event
from src.modules.events import events
from src.modules.help import help
from src.modules.leaderboard import leaderboard
from src.modules.profile import profile
from src.modules.scope import scope
from src.modules.user import user
from src.modules.version import version
from src.banner import banner
from src.static import KEY, SECRET

def main():
    print()
    if KEY is None:
        print("Environment variable ETHIACK_API_KEY is not set!")
        sys.exit()
    if SECRET is None:
        print("Environment variable ETHIACK_API_SECRET is not set!")
        sys.exit()
    
    if (len(sys.argv) < 2):
        print(banner())
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