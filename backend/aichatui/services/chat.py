from sqlalchemy.orm import Session

from aichatui.models import Chat


def update(chat: Chat, title: str, db: Session):
    chat.title = title

    db.commit()

    return chat


def delete(chat: Chat, db: Session):
    db.delete(chat)
    db.commit()


# TODO use chat contents
def generate_title_prompt(chat: Chat, db: Session):
    

    prompt = """### Task:
Generate a concise, 2-3 word title with an emoji summarizing the chat history.
### Guidelines:
- The title should clearly represent the main theme or subject of the conversation.
- Use emojis that enhance understanding of the topic, but avoid quotation marks or special formatting. Put the emoji at the start.
- Write the title in the chat's primary language which is dutch or english; default to English if needed.
- Prioritize accuracy over excessive creativity; keep it clear and simple.
- Your entire response must consist solely of the JSON object, without any introductory or concluding text.
- The output must be a single, raw JSON object, without any markdown code fences or other encapsulating text.
- Ensure no conversational text, affirmations, or explanations precede or follow the raw JSON output, as this will cause direct parsing failure.
### Output:
JSON format: { "title": "your concise title here" }
### Examples:
- { "title": "📉 Stock Market Trends" },
- { "title": "🍪 Chocolate Chip Recipe" },
- { "title": "🎵 Music Streaming Evolution" },
- { "title": "💻 Work Productivity" },
- { "title": "🤖 AI in Healthcare" },
- { "title": "🎮 Game Development Insights" }
### Chat History:
<chat_history>
This is a hardcoded example for title generation
</chat_history>"""

    return prompt