from dataclasses import dataclass
import enum
from openai import OpenAI
from aichatui.models import Model


@dataclass
class Roles:
    ROLE_USER = "user"
    ROLE_ASSISTANT = "assistant"


def query(model: Model, messages: dict, stream=True):
    openai = OpenAI(
        api_key=model.provider.api_key,
        base_url=model.provider.url,
    )

    chat_completion = openai.chat.completions.create(
        model=model.name,
        messages=messages,
        stream=stream,
    )

    for event in chat_completion:
        yield event
