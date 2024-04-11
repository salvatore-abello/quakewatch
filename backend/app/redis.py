import redis
from .constants import REDIS_HOST, REDIS_PORT


def connect():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def get_requests_from_key():
    client = connect()

    

    client.close()