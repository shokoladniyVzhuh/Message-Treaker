# watcher/tg_client.py
import os
from telethon import TelegramClient, events
from watcher.settings import API_ID, API_HASH, SESSION

client = TelegramClient(SESSION, API_ID, API_HASH)

async def resolve_chat(chat_ref: str):
    """Resolve chat by username, link or numeric id"""
    try:
        return await client.get_entity(chat_ref)
    except Exception as e:
        print(f"Error resolving chat {chat_ref}: {e}")
        return None

def start_listening(handler):
    """Start listening for new messages with custom handler"""
    @client.on(events.NewMessage)
    async def on_new_message(event):
        try:
            text = event.message.message or ""
            chat = await event.get_chat()
            # Всегда используем числовой ID чата для консистентности
            chat_id = str(chat.id)
            await handler(event, text, chat_id, event.message.id)
        except Exception as e:
            print("Listener error:", e)

    return client


