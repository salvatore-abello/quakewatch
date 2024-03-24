import requests
from threading import Lock
from cachetools import TTLCache, cached
from . import constants as CONSTANTS


@cached(cache=TTLCache(maxsize=640*512, getsizeof=len, ttl=3 * 60), lock=Lock()) # TTL 3min
def earthquake_query(data):
    data["format"] = "geojson"
    # TODO: Check if GET requests are enough
    return requests.request("GET", CONSTANTS.EARTHQUAKE_API_ENDPOINT, params=data).json()

# @cached(cache=TTLCache(maxsize=640*512, getsizeof=len, ttl=2 * 60 * 60), lock=Lock()) # TTL 1h
# def weather_query(data):
#     # pioggia moderata (4 – 6 mm/h) pioggia forte (> 6 mm/h) rovescio (> 10 mm/h) nubifragio (> 30 mm/h)
#     # https://api.3bmeteo.com/mobilev3/api_previsioni/home_geo/37.4226711/-122.0849872/en/0/1?format=json2&X-API-KEY=fhrwRdevqwq8r7q9UXTwP6lSX74g34jnQ6756tGo
#     # https://api.3bmeteo.com/mobilev3/api_previsioni/esaorario/5375480/1085/0/6/en/?format=json2&X-API-KEY=fhrwRdevqwq8r7q9UXTwP6lSX74g34jnQ6756tGo
#     # X-Api-Key: fhrwRdevqwq8r7q9UXTwP6lSX74g34jnQ6756tGo
#     # format: json2
#     # 
#     return {}

async def dispatch(query_type: str, data):
    if not (func:=ALLOWED_QUERY_TYPES.get(query_type)):
        return {"status": False, "data": {"msg": f"Unknown query type {query_type!r}"}}
    return func(data)
    
ALLOWED_QUERY_TYPES = {
    "earthquake": earthquake_query,
    # "weather": weather_query
}
