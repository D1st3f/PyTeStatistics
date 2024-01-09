import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from .exporter import CSVExporter
from .scraper import Scraper


class ChromeWebDriver:
    def __init__(self) -> None:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self._driver = webdriver.Chrome(options=chrome_options)

    def __enter__(self) -> WebDriver:
        return self._driver

    def __exit__(self,
                 exc_type: type,
                 exc_val: Exception,
                 exc_tb: type) -> None:
        self._driver.close()


def get_all_vacancy():
    logging.basicConfig(format='%(levelname)s - %(message)s',
                        level=logging.INFO)

    with ChromeWebDriver() as driver:
        scraper = Scraper(driver)
        all_vacancies = scraper.scrape_all_vacancies()
        filename = f'{datetime.now().strftime("Data %Y-%m-%d")}.csv'
        CSVExporter.export_to_csv(filename, all_vacancies)
