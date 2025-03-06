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
BASE_URL = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata/"

# Validate environment variables
if not TELEGRAM_API_TOKEN or not TELEGRAM_CHAT_ID:
    logging.error("Telegram API token or chat ID not found in environment variables.")
    exit(1)

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

def main():
    """Main function to fetch the Fear & Greed Index and send a Telegram message."""
    index_value = get_fear_greed_index()
    if index_value is not None and index_value <= 25:
        message = f"📊 CNN Fear & Greed Index: {index_value}\n🔗 Link: https://edition.cnn.com/markets/fear-and-greed"
        send_telegram_message(message)
    else:
        logging.info(f"Fear & Greed Index is {index_value}. No message sent.")

if __name__ == "__main__":
    main()
