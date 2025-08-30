from openai import OpenAI
from aichatui.models import Model


def query(model: Model, query: str):
    openai = OpenAI(
        api_key=model.provider.api_key,
        base_url=model.provider.url,
    )

    chat_completion = openai.chat.completions.create(
        model=model.name,
        messages=[{"role": "user", "content": query}],
        stream=True,
    )

    for event in chat_completion:
        if event.choices[0].finish_reason:
            print('usage: ', event.choices[0].finish_reason, event.usage.completion_tokens, event.usage.prompt_tokens, event.usage.total_tokens)

        else:
            if content:= event.choices[0].delta.content:
                yield content