import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

__version__ = "1.0.1"

KEY = os.getenv("ETHIACK_API_KEY")
SECRET = os.getenv("ETHIACK_API_SECRET")
AUTH = HTTPBasicAuth(KEY, SECRET)
API_URL = "https://api.ethiack.com/v1"
GQL_URL = "https://gql.ethiack.com/graphql"