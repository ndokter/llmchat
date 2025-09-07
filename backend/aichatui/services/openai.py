from openai import OpenAI
from aichatui.models import Model


def query(model: Model, messages: dict):
    openai = OpenAI(
        api_key=model.provider.api_key,
        base_url=model.provider.url,
    )

    chat_completion = openai.chat.completions.create(
        model=model.name,
        messages=messages,
        stream=True,
    )

    for event in chat_completion:
        yield event