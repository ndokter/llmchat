import redis
import redis.asyncio as aioredis
import json


class EventType:
    CHAT_TITLE = "chat:title"
    CHAT_COMPLETION = "chat:completion"
    CHAT_CREATED = "chat:created"


class PubSubProducer:
    def __init__(self, redis_url: str, channel: str):
        self.r = redis.from_url(redis_url, decode_responses=False)
        self.channel = channel

    def send(self, payload: dict) -> int:
        return self.r.publish(self.channel, json.dumps(payload))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.r.close()


class PubSubConsumer:
    def __init__(self, redis_url: str, channel: str):
        self.url = redis_url
        self.channel = channel

    async def __aenter__(self):
        self.redis = aioredis.from_url(self.url)
        self.ps = self.redis.pubsub()
        await self.ps.subscribe(self.channel)
        await self.ps.wait_subscribed()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.ps.close()
        await self.redis.close()

    def __aiter__(self):
        return self

    async def __anext__(self):
        msg = await self.ps.get_message(
            ignore_subscribe_messages=True,
            timeout=5
        )
        if msg is None:
            return None
        return json.loads(msg["data"])