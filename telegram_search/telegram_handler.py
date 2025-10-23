# telegram_handler.py (Final and Most Stable Version)

import asyncio
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import ChatAdminRequiredError

# NOTE: The global client variable has been REMOVED.

async def fetch_all_chats(api_id, api_hash, session_file):
    """Creates a client, fetches chats, and disconnects."""
    client = TelegramClient(session_file, api_id, api_hash)
    try:
        await client.connect()
        if not await client.is_user_authorized():
            raise Exception("Client not authorized. Please run 'python login.py' to log in.")
        
        dialogs = await client.get_dialogs()
        chats = [{"id": d.id, "name": d.name} for d in dialogs if d.is_channel or d.is_group]
        return sorted(chats, key=lambda x: x['name'])
    finally:
        if client.is_connected():
            await client.disconnect()

async def search_messages(api_id, api_hash, session_file, keywords, chat_ids, start_date, end_date, limit):
    """Creates a client, searches for messages, and disconnects."""
    print("\n--- Starting Search ---")
    print(f"Keywords: {keywords}, Start: {start_date}, End: {end_date}")
    
    client = TelegramClient(session_file, api_id, api_hash)
    matched_messages = []
    try:
        await client.connect()
        if not await client.is_user_authorized():
            raise Exception("Client not authorized. Please run 'python login.py' to log in.")

        for chat_id in chat_ids:
            try:
                entity = await client.get_entity(chat_id)
                print(f"\nSearching in chat: '{entity.title}'")
                for keyword in keywords:
                    print(f"  - Searching for keyword: '{keyword}'")
                    # ... (rest of the search logic is the same)
                    async for message in client.iter_messages(
                        entity, search=keyword, limit=limit, offset_date=end_date
                    ):
                        print(f"    > Found potential match: '{message.text[:50]}...' with date {message.date.date()}")
                        if start_date and message.date.date() < start_date:
                            print("      ... SKIPPING: Message is older than start date.")
                            continue
                        
                        print("      ... ACCEPTING message.")
                        author = "Unknown"
                        if message.sender:
                             author = getattr(message.sender, 'first_name', '') or ''
                             if getattr(message.sender, 'last_name', ''):
                                 author += f" {message.sender.last_name}"
                        
                        if message.text:
                            matched_messages.append({
                                "chat_name": entity.title, "author": author.strip(),
                                "timestamp": message.date.strftime('%Y-%m-%d %H:%M:%S'), "text": message.text
                            })
            except Exception as e:
                print(f"An error occurred with chat ID {chat_id}: {e}")
                continue
    finally:
        if client.is_connected():
            print("--- Search Finished, Disconnecting Client ---")
            await client.disconnect()
            
    matched_messages.sort(key=lambda x: x['timestamp'], reverse=True)
    return matched_messages