from setup_driver import setup_driver
from scrapping_functions import scraper
from regex_functions import regex_scrap
Setup = setup_driver.DriverSetup()
Driver = Setup.driver_set_browser(Setup.set_up_options())
Setup.driver_logging(Driver)

Scrap = scraper.TwitterScraper(50, 'ele', 'Livro')
search_scrap = Scrap.search_querys(Driver)

Regex = regex_scrap.ScrapRegex(50, 'ele', 'Livro')
timeline_regex = Regex.scrap_filter(Scrap.scrap_tweets_timeline(Driver))
Regex.organize_scrap_infos(timeline_regex)

search_regex = Regex.scrap_filter(Scrap.search_querys(Driver))
Regex.organize_scrap_infos(search_regex)

