# login.py
import configparser
from telethon.sync import TelegramClient

print("--- Starting One-Time Telegram Login ---")

# Read the API credentials from your config file
config = configparser.ConfigParser()
config.read('config.ini')
api_id = int(config['telegram']['api_id'])
api_hash = config['telegram']['api_hash']
session_name = "telegram_session"

# This 'with' block will create the client, connect,
# prompt you for your details if needed, and then disconnect.
with TelegramClient(session_name, api_id, api_hash) as client:
    print(f"\nSession file '{session_name}.session' will be created or updated.")
    # The client.is_connected() call is enough to trigger the login prompts
    # if you are not already authorized.
    if client.is_connected():
         print("Successfully connected to Telegram.")
         print("Your session file has been created. You can now run the web app.")
    else:
         print("Could not connect to Telegram.")