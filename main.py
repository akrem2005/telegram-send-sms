from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact
import asyncio
import os

app = Flask(__name__)

# Replace these with your credentials
api_id = '29433390'
api_hash = '95c71a35449348e4940087362aff698b'
phone_number = '+251929175653'
API_PASSWORD = "password"  # Use env variable or fallback

async def send_telegram_message(recipient_phone, message):
    client = TelegramClient('session_name', api_id, api_hash)
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
        
        # Send the message
        await client.send_message(recipient_phone, message)
        return {"status": "success", "message": f"Message sent to {recipient_phone}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        await client.disconnect()

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    password = data.get('password')
    recipient_phone = data.get('recipient_phone')
    message = data.get('message', 'Hello from Flask API!')
    
    if not password or password != API_PASSWORD:
        return jsonify({"status": "error", "message": "Invalid or missing password"}), 401
    
    if not recipient_phone:
        return jsonify({"status": "error", "message": "recipient_phone is required"}), 400
    
    # Run the async function in the event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(send_telegram_message(recipient_phone, message))
    loop.close()
    
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # Use PORT env variable or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)