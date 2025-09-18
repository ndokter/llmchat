from dataclasses import dataclass
import redis
import redis.asyncio as aioredis




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
    
    # def to_redis(self) -> Dict[str, str]:
    #     """
    #     Convert to plain dict[str, str] so it can be passed to
    #     redis-py xadd (which only accepts string values).
    #     """
    #     return {k: str(v) for k, v in asdict(self).items()}

    # @classmethod
    # def from_redis(cls, raw: Dict[str, str]) -> "ChatEvent":
    #     """Re-create the dataclass from redis reply."""
    #     return cls(**raw)


class EventStreamProducer:

    def __init__(self, redis_url, channel_name):
        self.redis_client = redis.from_url(redis_url)
        self.channel_name = channel_name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self

    def add_message(self, contents: dict):
        self.redis_client.xadd(
            self.channel_name,
            contents
        )


class EventStreamConsumer:

    def __init__(self, redis_url, channel_name):
        self.redis_client = aioredis.from_url(redis_url)
        self.channel_name = channel_name
        self.last_id = "0-0"
        self.block_ms = 5000

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return self

    def __aiter__(self):
        return self

    async def __anext__(self):
        messages = await self.redis_client.xread(
            {self.channel_name: self.last_id},
            count=10,
            block=self.block_ms,
        )

        if not messages:
            return None

        stream, message_list = messages[0]
        message_id, message_data = message_list[0]

        self.last_id = message_id.decode()
        decoded = {k.decode(): v.decode() for k, v in message_data.items()}

        await self.redis_client.xdel(stream, self.last_id)

        return decoded