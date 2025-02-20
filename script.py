from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# LINE Notify Token (Replace with your token)
LINE_NOTIFY_TOKEN = "3oNaBEXphV61pG4d7VRcvWv7eqcGlQyva83gVgIv9YC"

# CNN Fear & Greed Index URL
URL = "https://edition.cnn.com/markets/fear-and-greed"


def get_fear_greed_index():
        # Setup Chrome options (headless mode)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run without opening a browser
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Initialize WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Open CNN Fear & Greed Index page
    URL = "https://edition.cnn.com/markets/fear-and-greed"
    driver.get(URL)
    
    # Wait for the index value to load (adjust if necessary)
    driver.implicitly_wait(10)
    
    # Find the Fear & Greed Index value
    try:
        index_value = driver.find_element(By.CLASS_NAME, "market-fng-gauge__dial-number").text
        print("Fear & Greed Index:", index_value)
        return index_value
    except:
        print("Index value not found.")
    
    # Close the browser session
    driver.quit()

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
