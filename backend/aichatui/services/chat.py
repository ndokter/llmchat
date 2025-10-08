from sqlalchemy.orm import Session

from aichatui.models import Chat, ChatMessage

from sqlalchemy.orm import Session

from aichatui.config import settings
from aichatui.models import Chat, ChatMessage
from aichatui.models import ChatMessage
from aichatui.services.event_stream import PubSubProducer, EventType


def get_or_create(chat_id: int, db: Session):
    if chat_id:
        chat = db.get(Chat, chat_id)
    else:
        chat = Chat()
        db.add(chat)
        db.flush()

        # Trigger chat:created event
        with PubSubProducer(settings.REDIS_URL, channel="chat-events") as pub:
            pub.send({"type": EventType.CHAT_CREATED, "body": {"chat_id": chat.id}})

    return chat


def update(chat: Chat, title: str, db: Session):
    chat.title = title

    db.commit()

    return chat


def delete(chat: Chat, db: Session):
    db.delete(chat)
    db.commit()


# TODO use chat contents
def generate_title_prompt(chat: Chat, db: Session):

    user_message = (
        db.query(ChatMessage)
        .filter(ChatMessage.chat_id == chat.id, ChatMessage.role == "user")
        .order_by(ChatMessage.id.asc())
        .limit(1)
    ).first()

    assistant_message = (
        db.query(ChatMessage)
        .filter(ChatMessage.chat_id == chat.id, ChatMessage.role == "assistant")
        .order_by(ChatMessage.id.asc())
        .limit(1)
    ).first()

    def get_text_segments(text, max_chars=2000):
        if len(text) <= max_chars:
            return text
        else:
            half = max_chars // 2
            return text[:half] + text[-half:]
    
    user_segment = get_text_segments(user_message.message)
    assistant_segment = get_text_segments(assistant_message.message)
    
    prompt = f"""### Task:
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
JSON format: {{ "title": "your concise title here" }}
### Examples:
- {{ "title": "📉 Stock Market Trends" }},
- {{ "title": "🍪 Chocolate Chip Recipe" }},
- {{ "title": "🎵 Music Streaming Evolution" }},
- {{ "title": "💻 Work Productivity" }},
- {{ "title": "🤖 AI in Healthcare" }},
- {{ "title": "🎮 Game Development Insights" }}
### Chat History:
<chat_history>
{user_segment}
{assistant_segment}
</history>"""

    return prompt