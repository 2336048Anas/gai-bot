from telethon import TelegramClient, events
import requests
import json
from datetime import datetime
import asyncio
import os

# Debug environment variables
print("=== Environment Variables Debug ===")
print(f"API_ID: {os.getenv('API_ID', 'NOT FOUND')}")
print(f"API_HASH: {os.getenv('API_HASH', 'NOT FOUND')}")
print(f"GROUP_ID: {os.getenv('GROUP_ID', 'NOT FOUND')}")
print(f"DISCORD_WEBHOOK: {os.getenv('DISCORD_WEBHOOK', 'NOT FOUND')}")
print("================================")

# Get credentials from environment variables (for security)
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

# Convert api_id to int if it exists
if api_id:
    api_id = int(api_id)

# Ensure we have the required values
if not api_id or not api_hash:
    print("ERROR: Missing API_ID or API_HASH environment variables!")
    print("Please check your Railway environment variables.")
    exit(1)

group_ids = [int(os.getenv('GROUP_ID', '-1001950072056'))]
discord_webhook_url = os.getenv('DISCORD_WEBHOOK')

print(f"Using API_ID: {api_id}")
print(f"Using GROUP_ID: {group_ids[0]}")
print(f"Discord webhook configured: {'Yes' if discord_webhook_url else 'No'}")

# Initialize the client
client = TelegramClient('anon', api_id, api_hash)

def send_to_discord(message):
    """Send message to Discord using webhook"""
    data = {
        "content": f"@everyone 🚨 GAI Alert! 🚨\n\n{message}",
        "username": "GAI Monitor Bot"
    }
    try:
        response = requests.post(discord_webhook_url, json=data)
        if response.status_code == 204:
            return True
        else:
            print(f"Discord error: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error sending to Discord: {e}")
        return False

@client.on(events.NewMessage(chats=group_ids))
async def handler(event):
    message_text = event.message.message
    # Checking for the symbol in different formats and capitalizations
    symbols = ["$GAI", "GAI", "$gai", "gai", "graph", "Graph", "Graph AI", "graph AI"]

    now = datetime.now()
    print("running")
    print("Current Timestamp:", now)

    # Check if any GAI symbol appears anywhere in the message
    if any(symbol.lower() in message_text.lower() for symbol in symbols):
        # Send to Discord
        if send_to_discord(message_text):
            print(f"GAI found! Message sent to Discord: {message_text}")
        else:
            print(f"GAI found but failed to send to Discord: {message_text}")
    else:
        print("No GAI found in message, continuing...")

async def main():
    try:
        print("Starting GAI Monitor Bot...")
        await client.start()
        print("Successfully connected to Telegram!")
        print(f"Monitoring group: {group_ids[0]}")
        print("Bot is running - waiting for GAI mentions...")
        await client.run_until_disconnected()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    asyncio.run(main())
