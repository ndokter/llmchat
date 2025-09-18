from dataclasses import dataclass
import redis
import redis.asyncio as aioredis
import json



class EventType:
    CHAT_TITLE = "chat:title"
    CHAT_COMPLETION = "chat:completion"


@dataclass
class ChatEvent:
    type: EventType
    chat_id: str
    message_id: str
    status: str
    title: str
    content: str
    

class PubSubProducer:
    """Very small wrapper: open connection once, publish as JSON."""
    def __init__(self, redis_url: str, channel: str):
        self.r = redis.from_url(redis_url, decode_responses=False)
        self.ch = channel

    def send(self, payload: dict) -> int:
        """Returns # of clients that received the message."""
        return self.r.publish(self.ch, json.dumps(payload))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.r.close()


class PubSubConsumer:
    """Async generator that yields decoded dicts from the channel."""
    def __init__(self, redis_url: str, channel: str):
        self.url = redis_url
        self.ch = channel

    async def __aenter__(self):
        self.redis = aioredis.from_url(self.url)
        self.ps = self.redis.pubsub()
        await self.ps.subscribe(self.ch)
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