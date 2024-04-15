import redis
from .constants import REDIS_HOST, REDIS_PORT, LIMITS

def connect():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def delete_key(key):
    client = connect()

    plan_rate = LIMITS[key.plan.type]

    redis_key = f"LIMITS:LIMITER/{key.key}//query/earthquake/{'/1/'.join(plan_rate.split("/"))}"
    client.delete(redis_key)

    client.close()

def get_requests_number_from_key(key):
    client = connect()

    plan_rate = LIMITS[key.plan.type]
    parts = plan_rate.split("/")
    total = int(parts[0])

    redis_key = f"LIMITS:LIMITER/{key.key}//query/earthquake/{'/1/'.join(parts)}"
    res = client.get(redis_key)

    nreqs = int(res) if res else 0
    percentage = round(nreqs / total * 100, 2)

    client.close()

    return nreqs, percentage