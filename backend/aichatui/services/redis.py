import logging

import redis
import asyncio


logger = logging.getLogger(__name__)


class ChatMessageStreamProducer:
    """ Put chat message contents on a stream channel """

    def __init__(self, redis_url, channel_name):
        self.redis_client = redis.from_url(redis_url)
        self.channel_name = channel_name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.redis_client.xadd(
            self.channel_name,
            {"content": "", "status": "done"}
        )
        return False

    def add_message(self, content: str):
        self.redis_client.xadd(
            self.channel_name, 
            {"content": content, "status": "active"}
        )


class ChatMessageStreamConsumer:
    """ Consume chat message contents from channel """

    def __init__(self, redis_url, channel_name):
        self.redis_client = redis.from_url(redis_url)
        self.channel_name = channel_name
        self.last_id = '0-0'
        self.block_ms = 5000

        self._finished_successfully = False


    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await asyncio.to_thread(self.redis_client.delete, self.channel_name)

    def __aiter__(self):
        return self

    async def __anext__(self):
        # TODO native async client??
        messages = await asyncio.to_thread(
            self.redis_client.xread,
            {self.channel_name: self.last_id},
            count=1,
            block=self.block_ms
        )

        if not messages:
            return None

        _stream, message_list = messages[0]
        message_id, message_data = message_list[0]

        self.last_id = message_id.decode()

        decoded_data = {k.decode(): v.decode() for k, v in message_data.items()}

        if decoded_data.get("status") == "done":
            raise StopAsyncIteration

        return decoded_data