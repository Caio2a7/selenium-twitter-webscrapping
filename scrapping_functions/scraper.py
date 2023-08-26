from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.keys import Keys


class TwitterScraper:

    def __init__(self, tweets_amount: int, query_timeline_search: str, query_to_search: str):
        self.tweets_amount = tweets_amount
        self.query_timeline_search = query_timeline_search
        self.query_to_search = query_to_search

    def scrap_tweets_timeline(self, driver):
        timeline_list = []
        while True:
            try:
                timeline = driver.find_elements(By.CSS_SELECTOR, f'[data-testid="cellInnerDiv"]')
                for tweets_scrap in timeline:
                    timeline_list.append(tweets_scrap.text)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)
            except Exception:
                pass
            if len(timeline_list) > self.tweets_amount:
                break
        return timeline_list

    def search_querys(self, driver):
        sleep(2)
        driver.find_element(By.CSS_SELECTOR, '[data-testid="AppTabBar_Explore_Link"]').click()
        sleep(2)
        driver.find_element(By.CSS_SELECTOR, '[data-testid="SearchBox_Search_Input"]').send_keys(self.query_to_search)
        driver.find_element(By.CSS_SELECTOR, '[data-testid="SearchBox_Search_Input"]').send_keys(Keys.ENTER)
        sleep(4)
        search_scrap = self.scrap_tweets_timeline(driver)
        return search_scrap
