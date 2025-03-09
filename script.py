import os
import logging
from fake_useragent import UserAgent
import requests
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")
BASE_URL = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata/"

# Validate environment variables
if not TELEGRAM_API_TOKEN or not TELEGRAM_CHAT_ID:
    logging.error("Telegram API token or chat ID not found in environment variables.")
    exit(1)

# File to store the previous index value
PREVIOUS_INDEX_FILE = "previous_index.txt"

def get_fear_greed_index():
    """Fetches the CNN Fear & Greed Index."""
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
    }

    try:
        response = requests.get(BASE_URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        return round(data['fear_and_greed']['score'])
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching Fear & Greed Index: {e}")
        return None
    except (KeyError, json.JSONDecodeError) as e:
        logging.error(f"Error parsing Fear & Greed Index data: {e}")
        return None

def send_telegram_message(message):
    """Sends a message via Telegram."""
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(telegram_url, data=payload)
        response.raise_for_status()
        logging.info("Message sent successfully")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending Telegram message: {e}")
        logging.error(f"Response: {response.text}")  # Log the API response for debugging

def send_line_message(message):
    """Sends a message via LINE Notify"""
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
    data = {"message": message}
    requests.post(url, headers=headers, data=data)

def read_previous_index():
    """Reads the previous index value from a file."""
    try:
        with open(PREVIOUS_INDEX_FILE, "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return None

def write_previous_index(index):
    """Writes the current index value to a file."""
    with open(PREVIOUS_INDEX_FILE, "w") as file:
        file.write(str(index))

def main():
    """Main function to fetch the Fear & Greed Index and send a Telegram message."""
    index_value = get_fear_greed_index()
    if index_value is None:
        logging.error("Failed to fetch Fear & Greed Index.")
        return

    previous_index = read_previous_index()

    # Check if the index has changed
    if index_value != previous_index:
        message = f"📊 CNN Fear & Greed Index: {index_value}\n"
        if index_value <= 25:
            send_telegram_message(message)
            send_line_message(message)
        write_previous_index(index_value)  # Update the previous index value
        logging.info(f"Fear & Greed Index has changed to: {index_value}. Message sent.")
    else:
        logging.info(f"Fear & Greed Index is unchanged: {index_value}. No message sent.")

if __name__ == "__main__":
    main()
