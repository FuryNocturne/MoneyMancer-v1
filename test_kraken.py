import os
import krakenex
from dotenv import load_dotenv

load_dotenv()

api = krakenex.API()
api.key = os.getenv("KRAKEN_API_KEY")
api.secret = os.getenv("KRAKEN_API_SECRET")

res = api.query_private('Balance')
print("🔍 Balance API response:", res)
