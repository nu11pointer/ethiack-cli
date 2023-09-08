# Ethiack CLI Utility

## Index

1. [Description](#description)
2. [Usage](#usage)  
    2.1. [Windows](#windows)  
    2.2. [Unix](#unix)
3. [Installation](#installation)  
    3.1. [Requirements](#requirements)  
    3.2. [Windows Installation](#windows-installation)  
    3.3. [Unix Installation](#unix-installation)  
4. [Modules](#modules)  
    4.1. [event](#event)  
    4.2. [events](#events)  
    4.3. [help](#help)  
    4.4. [leaderboard](#leaderboard)  
    4.5. [profile](#profile)  
    4.6. [scope](#scope)  
    4.7. [user](#user)  
    4.8. [version](#version)  
5. [License](#license)

## Description

This is a (unofficial) utility that works as a client to the Ethiack platform. It allows you to perform multiple operations directly from the command-line.  
The tool uses the official [Ethiack API](https://api.ethiack.com/) and the [Ethiack's GraphQL](https://gql.ethiack.com/) endpoint to access the data it needs.  
It contains several modules so you can manage and view information related to your profile, users, leaderboard, events, etc.

## Usage

### Windows

After installing, just run `python3 ethiack.py` to use the utility.

### Unix

After installing, you can call `ethiack` directly from the command-line (since a symbolic link will be created during installation) or use python (`python3 ethiack.py`).

## Installation

### Requirements

- Python >= 3.10
- Ethiack API Key & Secret (you can get it from [here](https://portal.ethiack.com/settings/api))

### Windows Installation

1. Open Powershell in the same directory as the project
2. Run the installation file:

    ```ps1
    .\install.ps1
    ```

3. Export the required environment variables (don't forget to replace the values between double quotes):

    ```ps1
    echo 'ETHIACK_API_KEY="<api-key>"' > .env
    echo 'ETHIACK_API_SECRET="<api-secret>"' >> .env
    ```

    or

    ```ps1
    $env:ETHIACK_API_KEY = "<api-key>"
    $env:ETHIACK_API_SECRET = "<api-secret>"
    ```

### Unix Installation

1. Open a shell in the same directory as the project
2. Run the installation file:

    ```sh
    chmod +x install.sh
    ./install.sh
    ```

3. Export the required environment variables (don't forget to replace the values between double quotes):

    ```sh
    echo 'ETHIACK_API_KEY="<api-key>"' > .env
    echo 'ETHIACK_API_SECRET="<api-secret>"' >> .env
    ```

    or

    ```sh
    export ETHIACK_API_KEY="<api-key>"
    export ETHIACK_API_SECRET="<api-secret>"
    ```

4. Optionally, you can set the environment variables permanently (if you're not using the first option, in the previous process):

    (using ZSH shell)

    ```sh
    echo 'export ETHIACK_API_KEY="<api-key>"' >> .zshrc
    echo 'export ETHIACK_API_SECRET="<api-secret>"' >> .zshrc
    ```

    (using Bash shell)

    ```sh
    echo 'export ETHIACK_API_KEY="<api-key>"' >> .bashrc
    echo 'export ETHIACK_API_SECRET="<api-secret>"' >> .bashrc
    ```

## Modules

```txt
event <event>               Get information regarding a specific event
events [running]            Gets a list of events you're associated with
help                        Show the help page
leaderboard [country]       Hacker leaderboard
profile                     Your public profile
scope <event> [save]        Get the scope for an event
user <user>                 Get a user's public profile
version                     Show the utility version
```

### event

Allows you to get information from an event/program such as its dimension, category, start and end dates, physical location and status.

```txt
ethiack event example-p1

Event
----------------------------------------
ID: 1337
Slug: example-p1
Name: Example P1
Dimension: virtual
Category: pentest
Type: human
Start: Sat, 01 Jul 2023 15:00:00 GMT
End: Mon, 31 Jul 2023 18:00:00 GMT
Latitude:
Longitude:
Status: Retesting
----------------------------------------
```

### events

Get a list of all the events you've worked in. You can optionally pass `running` as a second parameter to only get a list of the running events.

```txt
ethiack events

Events
----------------------------------------
  ethiack-p1                  |  Ethiack P1
  ethiack-p2                  |  Ethiack P2
  example-rt1                 |  Example RT1
  example-p1                  |  Example P1
----------------------------------------
```

### help

Shows the help page, listing the modules available, their descriptions, and the parameters to be passed.

### leaderboard

Displays the leaderboard, detailing the rank position, points, username and country from each hacker. You can optionally pass the country code as a second parameter to only get a list of the leaderboard in that country.

```txt
ethiack leaderboard pt

Leaderboard (TOP 6)
----------------------------------------
  1.  | 31337                              | 701 | PT
  2.  | hackerman                          | 464 | PT
  3.  | fidgetspinner                      | 342 | PT
  4.  | artihacker                         | 320 | PT
  5.  | ethiacker                          | 237 | PT
  6.  | newbie                             | 73  | PT
----------------------------------------
```

### profile

Displays information from your profile in Ethiack. This contains data such as username, name, rank, points, VAT, role, entity type, join date, country and URL to portal.

```txt
ethiack profile

Profile
----------------------------------------
Username: hackerman
Name: Hacker Man
Rank: #2 (TOP 3)
Points: 464.48
VAT: PT 123456789
Role: hacker
Entity: individual
Joined at: 2023-06-08T22:52:18
Country: PT
URL: https://portal.ethiack.com/hackerman
----------------------------------------
```

### scope

Displays the scope of an event - in-scope and out-of-scope assets - such as domains, URLs, IP addresses, CIDR addresses, and wildcards. Optionally, you can pass the extra parameter `save` to save all the domains, IP addresses, URLs and wildcard domains to a text file `inscope.txt` and `outofscope.txt`.  

```txt
ethiack scope example-p1 save

Scope (example-p1)
----------------------------------------
  In-Scope
  --------------------------------------
    *.example.com                                               | domain
    qa.example.com                                              | domain | https://qa.example.com/juicy/
    dev.example.com                                             | domain | https://dev.example.com/juicy/

  Out-of-Scope
  --------------------------------------
    prod.example.com                                            | domain

File 'inscope.txt' saved!
File 'outofscope.txt' saved!
```

The file `inscope.txt` will contain the following content:

```txt
*.example.com
qa.example.com
dev.example.com
```

### user

Shows information from a user (can be a hacker, triager or an organization member or account). This contains data such as username, rank, points, role, entity type, join date, country and URL to portal.

```txt
ethiack user newbie

User
----------------------------------------
Username: newbie
Rank: #6 (TOP 10)
Points: 73.50
Role: hacker
Entity: individual
Joined at: 2023-09-08T15:30:18
Country: PT
URL: https://portal.ethiack.com/newbie
----------------------------------------
```

### version

Display the utility version.

```txt
ethiack version

ethiack-cli v1.0.0
```

## License

License is available [here](./LICENSE).
