from setup_driver import setup_driver
from scrapping_functions import scraper
from regex_functions import regex_scrap
from spreadsheet_maker import xlsx_maker
from email_sender import email_smtp
import json
with open("user_data.json", 'r') as json_file:
    data = json.load(json_file)

#Setuping the driver with the browser used, twitter email, password and username
Setup = setup_driver.DriverSetup(data['browser_name'], data['email'], data['password'],
                                 data['username'])
Driver = Setup.driver_set_browser(Setup.set_up_options())
Setup.driver_logging(Driver)

# Web scrapping 
Scrap = scraper.TwitterScraper(50, 'ele', 'Livro')
search_scrap = Scrap.search_querys(Driver)
# The execution of a regex function to filter the data scraped
Regex = regex_scrap.ScrapRegex(50, 'ele', 'Livro')
timeline_regex = Regex.scrap_filter(Scrap.scrap_tweets_timeline(Driver))
Regex.organize_scrap_infos(timeline_regex)
# Creating the spreadsheet file
excel = xlsx_maker.SpreadSheet(Regex.organize_scrap_infos(timeline_regex))
excel.create_excel()
# Email sending
email = email_smtp.EmailSender(data['client_email'])
email.email_usuario()
email.send_email()