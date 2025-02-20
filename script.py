import requests
from bs4 import BeautifulSoup
import json

# LINE Notify Token (Replace with your token)
LINE_NOTIFY_TOKEN = "3oNaBEXphV61pG4d7VRcvWv7eqcGlQyva83gVgIv9YC"

# CNN Fear & Greed Index URL
URL = "https://edition.cnn.com/markets/fear-and-greed"


def get_fear_greed_index():
    """Scrapes CNN's Fear & Greed Index"""
    response = requests.get(URL)
    if response.status_code != 200:
        return "Error fetching data"

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the index value in the page (adjust selector as needed)
    index_value = soup.find("div", class_="market-fng-gauge__dial-number").text.strip()

    return index_value


def send_line_message(message):
    """Sends a message via LINE Notify"""
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
    data = {"message": message}
    requests.post(url, headers=headers, data=data)


def main():
    index_value = get_fear_greed_index()
    message = f"📊 CNN Fear & Greed Index Today: {index_value}"
    send_line_message(message)


if __name__ == "__main__":
    main()
