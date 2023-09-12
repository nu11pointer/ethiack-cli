from src.banner import banner

def help():
    print(f"""{banner()}          

Modules:
    event <event>               Get information regarding a specific event
    events [running]            Gets a list of events you're associated with
    help                        Show the help page
    leaderboard [country]       Hacker leaderboard
    profile                     Your public profile
    scope <event> [save]        Get the scope of an event
    user <user>                 Get a user's public profile
    version                     Show the utility version""")