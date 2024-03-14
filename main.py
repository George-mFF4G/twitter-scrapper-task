
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def scrape_stock_mentions(twitter_accounts, stock_symbol, interval_minutes):
    try:
        PATH = "./chromedriver.exe"  
        URL = "https://twitter.com/"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        service = Service(PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://twitter.com")

        while True:
            total_mentions = 0
            for account in twitter_accounts:
                try:
                    finalURL = f"{URL}{account}"
                    driver.get(finalURL)
                    time.sleep(5)  
                    page_cards = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
                    for card in page_cards:
                        try:
                            tweet_text_element = card.find_element(By.XPATH, './/div[@dir="auto"]/span')
                            tweet_text = tweet_text_element.text
                            if stock_symbol in tweet_text:
                                total_mentions += 1
                        except NoSuchElementException as e:
                            print("Error parsing tweet text:", e)

                except Exception as e:
                    print("Error scraping account:", e)

            print(f"{stock_symbol} was mentioned {total_mentions} times in the last {interval_minutes} minutes.")
            time.sleep(interval_minutes * 60)

    except Exception as e:
        print("Error initializing driver:", e)
    finally:
        driver.quit()


def main():
    twitter_accounts = ["Mr_Derivatives", "warrior_0719", "ChartingProdigy", "allstarcharts", "yuriymatso",
                        "TriggerTrades", "AdamMancini4 ", "CordovaTrades", "Barchart",
                        "RoyLMattox"]  
    stock_symbol = "$TSLA" 
    interval_minutes = 15  
    scrape_stock_mentions(twitter_accounts, stock_symbol, interval_minutes)


if __name__ == "__main__":
    main()