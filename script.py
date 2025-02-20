
# LINE Notify Token (Replace with your token)
LINE_NOTIFY_TOKEN = "3oNaBEXphV61pG4d7VRcvWv7eqcGlQyva83gVgIv9YC"

# CNN Fear & Greed Index URL
URL = "https://edition.cnn.com/markets/fear-and-greed"


def get_fear_greed_index():


def send_line_message(message):
    """Sends a message via LINE Notify"""
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
    data = {"message": message}
    requests.post(url, headers=headers, data=data)


def main():
    index_value = get_fear_greed_index()
    message = f"📊 CNN Fear & Greed Index Today: {index_value} : {https://edition.cnn.com/markets/fear-and-greed}"
    send_line_message(message)


if __name__ == "__main__":
    main()
