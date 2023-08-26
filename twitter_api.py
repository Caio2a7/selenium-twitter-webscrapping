from selenium import webdriver
import openpyxl
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions, FirefoxOptions, IeOptions, EdgeOptions
from selenium.webdriver.common.keys import Keys
from time import sleep
import re


class TwitterScraper:

    def __init__(self, browser_name: str, email: str, password: str, user: str):
        self.browser_name = browser_name
        self.email = email
        self.password = password
        self.user = user
        self.data = []

    def __add__(self, tweets_amount, query_timeline_search, query_to_search):
        self.tweets_amount = tweets_amount
        self.query_timeline_search = query_timeline_search
        self.query_to_search = query_to_search

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
        driver.find_element(By.CSS_SELECTOR, '[data-testid="ocfEnterTextTextInput"]').send_keys(self.user)
        driver.find_element(By.CSS_SELECTOR, '[data-testid="ocfEnterTextNextButton"]').click()
        sleep(3)
        driver.find_element(By.NAME, 'password').send_keys(self.password)
        driver.find_element(By.CSS_SELECTOR, '[data-testid="LoginForm_Login_Button"]').click()
        sleep(5)

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
        regex_search_scrap = self.scrap_filter(search_scrap)
        return regex_search_scrap

    def scrap_filter(self, tweets_list):
        regex_list = []
        for tweets in tweets_list:
            regex = re.findall(fr'{self.query_timeline_search}', tweets)
            regex_list.append(regex)
        index_list = [regex_list.index(link) for link in regex_list if link != []]
        tweets_links = [tweets_list[i] for i in index_list]
        regex_list = [elements for elements in regex_list if elements != []]
        print(f'The number of occurencies of "{self.query_timeline_search}" in '
              f'{self.tweets_amount} tweets was: {len(regex_list)}\n')
        correct_tweets_links = list(set(tweets_links))
        return correct_tweets_links

    def organize_scrap_infos(self, scrap_info):
        for tweets in scrap_info:
            tweets_splited = tweets.split('\n')
            tweets_number_info = {'Comments': tweets_splited[-4] if len(tweets_splited[-4]) < 10 else 0,
                                  'Replys': tweets_splited[-3] if len(tweets_splited[-3]) < 10 else 0,
                                  'Likes': tweets_splited[-2] if len(tweets_splited[-2]) < 10 else 0,
                                  'Views': tweets_splited[-1] if len(tweets_splited[-1]) < 12 else 0}
            tweets_user_info = {'Username': tweets_splited[:2]}
            for remove in range(3):
                del tweets_splited[0]
            for deletion in range(3):
                del tweets_splited[-1]
            tweets_text_info = " ".join(tweets_splited)
            tweets_user_joined = " ".join(tweets_user_info['Username'])
            print(f'{tweets_user_joined} {tweets_number_info} {tweets_text_info}')
            self.data.append({'Username': tweets_user_info['Username'],
                              'Comments': tweets_number_info['Comments'],
                              'Replys': tweets_number_info['Replys'],
                              'Likes': tweets_number_info['Likes'],
                              'Views': tweets_number_info['Views'],
                              'Text': tweets_text_info})

    def create_excel(self):
        df = pd.DataFrame(self.data)
        df.to_excel('twitter_scrap.xlsx', index=False)

    def email_usuario(self):
        print('OKUSUERE')
        self.email = input(
            'Digite o email para receber o relatorio de valores dos celulares!\n')
        self.email.lower()

        padrao = re.search(
            r'[a-zA-Z0-9_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{1,3}$', self.email)
        if padrao:
            print('email Valido')

        else:
            print('Digite um email valido!!!')
            self.email_usuario()

    def send_email(self):
        endereco_remetente = 'senDERemai2@outlook.com'
        senha_remetente = "Senderemailbot4"
        endereco_destinatario = 'caiodanielfonseca@gmail.com'

        # Crie o objeto do email
        msg = MIMEMultipart()
        msg['From'] = endereco_remetente
        msg['To'] = endereco_destinatario
        msg['Subject'] = 'Email com Anexo'

        # Adicione um corpo ao email (opcional)
        corpo_email = "Olá, este é um email com um arquivo Excel anexado."
        msg.attach(MIMEText(corpo_email, 'plain'))
        arquivo_excel = 'twitter_scrap.xlsx'
        with open(arquivo_excel, 'rb') as file:
            anexo = MIMEApplication(file.read(), Name='exemplo_pandas_excel.xlsx')
        anexo['Content-Disposition'] = f'attachment; filename="{arquivo_excel}"'
        msg.attach(anexo)
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(endereco_remetente, senha_remetente)
        server.sendmail(endereco_remetente, endereco_destinatario, msg.as_string())
        server.quit()


Setup = TwitterScraper()
Setup.__add__(50, 'ele', 'Livro')
Driver = Setup.driver_set_browser(Setup.set_up_options())
Setup.driver_logging(Driver)
scrap_list = Setup.scrap_tweets_timeline(Driver)

Scrap_info = Setup.scrap_filter(scrap_list)
Setup.organize_scrap_infos(Scrap_info)

Setup.create_excel()
Setup.send_email()
