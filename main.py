import requests
from datetime import datetime
import time
from flask import Flask
from threading import Thread

# Your Telegram Bot Token and User ID
BOT_TOKEN = '7625796624:AAFtBxQx7eX_owHBL6Sco8OTrQ3uUw43rX4'
USER_ID = '1467688672'
GOAL_DATE = datetime(2026, 2, 20)

# Your hosted app URL (used for self-ping)
APP_URL = "https://f7f918b0-f4ce-4e8b-9775-5c88c4b83cf1-00-1qfl8dbvnxonn.sisko.replit.dev/"

# Flask server to keep Replit alive
app = Flask('')


@app.route('/')
def home():
    return "Bot is running!"


def run():
    app.run(host='0.0.0.0', port=8080)


# Function to send Telegram message
def send_telegram_message(text):
    try:
        # Send the message
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {'chat_id': USER_ID, 'text': text}
        response = requests.post(url, data=data)
        response_json = response.json()

        if not response.ok:
            print(f"Telegram API Error: {response_json}")
            return

        print(f"Message sent successfully: {text}")
    except Exception as e:
        print(f"Error sending message - Full error: {str(e)}")


# Self-ping to keep the app alive
def self_ping():
    while True:
        try:
            print("🔄 Self-pinging to keep app alive...")
            requests.get(APP_URL)
        except Exception as e:
            print(f"❌ Self-ping failed: {e}")
        time.sleep(300)  # ping every 5 minutes


# Start the Flask server
Thread(target=run).start()

# Start self-pinging in a separate thread
Thread(target=self_ping).start()

# List of motivational messages
messages = [
    "Keep pushing forward — your future self is cheering for you! 💪",
    "Every line of code you write is a step closer to your dream. 🚀",
    "Success comes from consistent effort, not sudden greatness. 🔁",
    "You're not just learning to code — you're building your future! 🏗️",
    "Great developers weren’t born, they were made. Keep going! 🔥",
    "Progress is progress, no matter how small. 👣",
    "Discipline > Motivation. Wake up, show up, grow up. 🌱",
    "Debug your doubts — your vision is valid. 🐞✨",
    "You have 24 hours today. Invest at least one in your dream. ⏳",
    "Your goal is waiting. Don’t let comfort zones delay it. 🧗"
]

# Send initial message to confirm bot is working
send_telegram_message("Bot started! 🚀")

# Main loop
while True:
    try:
        now = datetime.utcnow()
        print(f"[⏰ UTC Time Check] {now}")

        if now.hour == 23 and now.minute == 0:  # 5:00 AM BD = 11:00 PM UTC
            # Countdown
            days_remaining = (GOAL_DATE - now).days

            # Pick message of the day
            index = now.timetuple().tm_yday % len(messages)
            daily_message = messages[index]

            # Final composed message
            message = (f"🌄 Good morning, developer!\n"
                       f"{days_remaining} days left until your goal. 🎯\n\n"
                       f"{daily_message}")

            # Send message
            send_telegram_message(message)

            # Prevent double sending
            time.sleep(60)

        # Check every 30 seconds
        time.sleep(30)
    except Exception as e:
        print(f"❌ Error in main loop: {e}")
        time.sleep(60)
