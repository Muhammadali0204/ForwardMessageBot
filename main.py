import asyncio
from random import randint

from decouple import Config, Csv
from contextlib import suppress
from telethon import TelegramClient, events, types

env = Config('.env')

API_ID = env("API_ID", cast=int)
API_HASH = env("API_HASH", cast=str)
KEYWORDS = env("KEYWORDS", cast=Csv(str))
SOURCE_GROUPS = env("SOURCE_GROUPS", cast=Csv(int))
DEST_GROUP_ID = env("DEST_GROUP_ID", cast=int)

client = TelegramClient("session", API_ID, API_HASH)

async def main():
    await client.start()
    await client.run_until_disconnected()

@client.on(events.NewMessage(chats=SOURCE_GROUPS))
async def handler(event: types.UpdateNewChannelMessage):
    text = event.message.message.lower() if event.message.message else ""

    if any(keyword in text for keyword in KEYWORDS):
        await asyncio.sleep(randint(1, 5))
        await event.message.forward_to(DEST_GROUP_ID)

if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
