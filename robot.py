# The only reason this is its own file is to stop circular imports.

from config import CONSUMER_KEY, REDIRECT_URI, JSON_PATH
from td.client import TDClient

td_client = TDClient(
    client_id=CONSUMER_KEY,
    redirect_uri=REDIRECT_URI,
    credentials_path=JSON_PATH
)
td_client.login()
print("Logged in")

