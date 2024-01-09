import logging
from dataclasses import dataclass
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from config import BASE_URL


@dataclass
class VacancyItem:
    title: str
    text: str
    location: str
    experience: int
    created: datetime
    views: int
    applications: int


class Scraper:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def get_current_page_number(self) -> str:
        current_page = self.driver.find_element(
            By.CSS_SELECTOR,
            "ul.pagination.pagination_with_numbers > "
            "li.page-item.active > span.page-link"
        )
        return current_page.text.replace("\n(current)", "")

    def next_page(self) -> bool:
        buttons_menu = self.driver.find_elements(By.CLASS_NAME,
                                                 "page-link")
        if not buttons_menu[-1].get_attribute("aria-disabled"):
            self.driver.execute_script("arguments[0].click();",
                                       buttons_menu[-1])
            return True

    @staticmethod
    def parse_vacancy(vacancy) -> VacancyItem:
        title = vacancy.find_element(By.CLASS_NAME, "job-list-item__link").text
        text = vacancy.find_element(
            By.CSS_SELECTOR,
            "div.job-list-item__description > span"
        ).get_attribute("data-original-text")
        location = vacancy.find_element(By.CLASS_NAME, "location-text").text
        experience = 0
        choices = vacancy.find_elements(
            By.CSS_SELECTOR,
            "div.job-list-item__job-info.font-weight-500 > span.nobr"
        )
        for choice in choices:
            if "досвід" in choice.text:
                for digit in choice.text.split():
                    if digit.isdigit():
                        experience = int(digit)
                        break
        created = vacancy.find_element(
            By.CSS_SELECTOR,
            "div.d-flex.align-items-center.font-size-small.mb-2 > "
            "span.job-list-item__counts.d-none.d-lg-inline-block.nobr > "
            "span > span.mr-2.nobr"
        ).get_attribute("data-original-title")
        views = vacancy.find_element(
            By.CSS_SELECTOR,
            "div.d-flex.align-items-center.font-size-small.mb-2 > "
            "span.job-list-item__counts.d-none.d-lg-inline-block.nobr > "
            "span > span:nth-child(2) > span:nth-child(1)"
        ).get_attribute("data-original-title").split(" ")[0]
        applications = vacancy.find_element(
            By.CSS_SELECTOR,
            "div.d-flex.align-items-center.font-size-small.mb-2 > "
            "span.job-list-item__counts.d-none.d-lg-inline-block.nobr > "
            "span > span:nth-child(2) > span:nth-child(2)"
        ).get_attribute("data-original-title").split(" ")[0]
        return VacancyItem(
            title=title,
            text=text,
            experience=experience,
            location=location,
            created=datetime.strptime(created, "%H:%M %d.%m.%Y"),
            views=int(views),
            applications=int(applications)
        )

    def parse_all_vacancies(self) -> [VacancyItem]:
        all_vacancies_card = self.driver.find_elements(By.CLASS_NAME,
                                                       "job-list-item")
        return [self.parse_vacancy(vacancy) for vacancy in all_vacancies_card]

    def scrape_all_vacancies(self) -> [VacancyItem]:
        logging.info("Parsing started!")
        all_vacancies = []
        self.driver.get(BASE_URL)
        all_vacancies.extend(self.parse_all_vacancies())
        logging.info(f"Page {self.get_current_page_number()} was parsed!")
        while self.next_page():
            logging.info(f"Page {self.get_current_page_number()} was parsed!")
            all_vacancies.extend(self.parse_all_vacancies())
        logging.info("Parsing done!")
        return all_vacancies
