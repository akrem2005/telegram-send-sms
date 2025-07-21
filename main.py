from telethon import TelegramClient, sync
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact

# Replace these with your credentials
api_id = '29433390'  # e.g., 123456
api_hash = '95c71a35449348e4940087362aff698b'  # e.g., '1234567890abcdef1234567890abcdef'
phone_number = '+251929175653'  # e.g., '+1234567890'
recipient_phone = '+251982547791'  # e.g., '+0987654321'
message = 'S'

# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

async def send_message_to_phone():
    try:
        # Start the client
        await client.start(phone=phone_number)
        
        # Add recipient to contacts (optional, if not already added)
        contact = InputPhoneContact(
            client_id=0,
            phone=recipient_phone,
            first_name='Recipient',
            last_name=''
        )
        result = await client(ImportContactsRequest([contact]))
        
        # Check if contact was added successfully
        if result.imported:
            print(f"Added {recipient_phone} to contacts.")
        else:
            print(f"Contact {recipient_phone} already exists or is not on Telegram.")
        
        # Send the message
        await client.send_message(recipient_phone, message)
        print(f"Message sent to {recipient_phone}: {message}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.disconnect()

# Run the async function
if __name__ == '__main__':
    client.loop.run_until_complete(send_message_to_phone())