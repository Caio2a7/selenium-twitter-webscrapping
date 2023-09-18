from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, IeOptions, EdgeOptions
from selenium.webdriver.common.by import By
from time import sleep


class DriverSetup:

    def __init__(self, browser_name: str, email: str, password: str, user: str):
        self.browser_name = browser_name
        self.email = email
        self.password = password
        self.user = user

    def set_up_options(self):
        chosed_browser_options = []
        match self.browser_name:
            case 'Chrome':
                chosed_browser_options.append(ChromeOptions())
            case 'Firefox':
                chosed_browser_options.append(FirefoxOptions())
            case 'Edge':
                chosed_browser_options.append(IeOptions())
            case 'Explorer':
                chosed_browser_options.append(EdgeOptions())
        browser_options = chosed_browser_options[0]
        browser_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        browser_options.add_argument('--lang=pr-BR')
        browser_options.add_argument('--disable-notifications')
        browser_options.add_argument('--disable-popup-blocking')
        browser_options.add_argument('--ignore-certificate-errors')
        browser_options.add_argument('--no-sandbox')

    def driver_set_browser(self, browser_options):
        chosed_driver = []
        match self.browser_name:
            case 'Chrome':
                chosed_driver.append(webdriver.Chrome(options=browser_options))
            case 'Firefox':
                chosed_driver.append(webdriver.Firefox(options=browser_options))
            case 'Edge':
                chosed_driver.append(webdriver.Edge(options=browser_options))
            case 'Explorer':
                chosed_driver.append(webdriver.Ie(options=browser_options))
        driver = chosed_driver[0]
        driver.get('https://twitter.com/home')
        driver.set_window_size(800, 700)
        return driver

    def driver_logging(self, driver):
        sleep(4)
        driver.find_element(By.NAME, 'text').send_keys(self.email)
        driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]'
                                          '/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]').click()
        sleep(3)
        try:
            driver.find_element(By.CSS_SELECTOR, '[data-testid="ocfEnterTextTextInput"]').send_keys(self.user)
            driver.find_element(By.CSS_SELECTOR, '[data-testid="ocfEnterTextNextButton"]').click()
            sleep(3)
        except Exception:
            driver.find_element(By.NAME, 'password').send_keys(self.password)
            driver.find_element(By.CSS_SELECTOR, '[data-testid="LoginForm_Login_Button"]').click()
            sleep(5)
            driver.find_element(By.CSS_SELECTOR, '[data-testid="ocfEnterTextTextInput"]').send_keys(self.user)
            driver.find_element(By.CSS_SELECTOR, '[data-testid="ocfEnterTextNextButton"]').click()
            sleep(3)
        else:
            driver.find_element(By.NAME, 'password').send_keys(self.password)
            driver.find_element(By.CSS_SELECTOR, '[data-testid="LoginForm_Login_Button"]').click()
            sleep(5)