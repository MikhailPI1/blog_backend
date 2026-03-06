import redis
from ..config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    password=REDIS_PASSWORD,
    decode_responses=True
)

try:
    r.ping()
    print("Successful connect to Redis")
except redis.ConnectionError:
    print("Error connect to Redis")