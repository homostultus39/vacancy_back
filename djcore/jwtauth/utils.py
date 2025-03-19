import redis
from django.conf import settings

redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])

def blacklist_token(token, expires_in) -> None:
    redis_client.setex(f"blacklist:{token}", expires_in, "blacklisted")

def is_blacklisted(token) -> bool:
    is_exists = True if redis_client.exists(f"blacklist:{token}") else False
    return is_exists
