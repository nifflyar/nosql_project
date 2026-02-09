import json
from redis.asyncio import Redis
from core.config import settings


redis = Redis.from_url(settings.REDIS_URL_DOCKER, decode_responses=True)


async def get_redis() -> Redis:
    return redis


async def delete_from_redis(key):
    product = await redis.get(key)
    if product:
        await redis.delete(key)


async def update_redis(key, data):
    await delete_from_redis(key)
    await redis.setex(key, 300, json.dumps(data))
