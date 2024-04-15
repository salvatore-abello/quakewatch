import os
import json
import requests
from threading import Lock
from cachetools import TTLCache, Cache, cached
from . import constants as CONSTANTS


@cached(cache=TTLCache(maxsize=640*512, getsizeof=len, ttl=3 * 60), lock=Lock()) # TTL 3min
def earthquake_query(data):
    data["format"] = "geojson"
    return requests.request("GET", CONSTANTS.EARTHQUAKE_API_ENDPOINT, params=data, headers={'Cache-Control': 'no-cache'}).json()

@cached(cache=Cache(maxsize=640*512), lock=Lock())
def get_free_earthquake_data():
    with open(os.path.join("/app", "static", "files", "query-example.json"), "r") as f:
        return json.loads(f.read())

async def dispatch(query_type: str, data):
    if not (func:=ALLOWED_QUERY_TYPES.get(query_type)):
        return {"status": False, "data": {"msg": f"Unknown query type {query_type!r}"}}
    return func(data)
    
ALLOWED_QUERY_TYPES = {
    "earthquake": earthquake_query,
    # In case you want to add features, just add the function names below
    # Eg:
    # "weather": weather_query
}
