import os
import asyncio
from random import randint

from contextlib import suppress
from dotenv import load_dotenv
from telethon import TelegramClient, events, types

load_dotenv('.env')

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
KEYWORDS = os.getenv("KEYWORDS").split(',')
DEST_GROUP_ID = int(os.getenv("DEST_GROUP_ID"))

client = TelegramClient("session", API_ID, API_HASH)

SOURCE_GROUP_IDS = set()


async def build_archived_groups(client: TelegramClient):
    ids = set()
    async for d in client.iter_dialogs(folder=1):
        if d.is_group:
            ids.add(d.entity.id)
    return ids


async def handler(event: types.UpdateNewChannelMessage):
    text = event.message.message.lower() if event.message.message else ""

    if any(keyword in text for keyword in KEYWORDS):
        await asyncio.sleep(randint(1, 5))
        await forward_message(event.message)
        return

    media = event.message.media
    if media and hasattr(media, 'document'):
        document = media.document
        if document and document.mime_type.startswith('audio/'):
            await asyncio.sleep(randint(1, 5))
            await forward_message(event.message)


async def forward_message(message):
    try :
        await message.forward_to(DEST_GROUP_ID)
    except:
        pass

async def main():
    await client.start()

    global SOURCE_GROUP_IDS
    SOURCE_GROUP_IDS = await build_archived_groups(client)

    client.add_event_handler(handler, events.NewMessage(chats=SOURCE_GROUP_IDS))

    await client.run_until_disconnected()


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
