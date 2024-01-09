import csv
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

BASE_URL = "https://djinni.co"
PYTHON_URL = urljoin(BASE_URL, "/jobs/?primary_keyword=Python")


@dataclass
class VacancyItem:
    title: str
    text: str
    location: str
    experience: int
    created: datetime
    views: int
    applications: int


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


def export_to_csv(file_name: str, vacancies: list[VacancyItem]) -> None:
    with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title",
                      "text",
                      "location",
                      "experience",
                      "created",
                      "views",
                      "applications"]
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fieldnames)
        for vacancy in vacancies:
            csvwriter.writerow([vacancy.title,
                                vacancy.text,
                                vacancy.location,
                                vacancy.experience,
                                vacancy.created,
                                vacancy.views,
                                vacancy.applications])


def get_current_page_number(driver) -> str:
    current_page = driver.find_element(
        By.CSS_SELECTOR,
        "ul.pagination.pagination_with_numbers > "
        "li.page-item.active > "
        "span.page-link"
    )
    return current_page.text.replace("\n(current)", "")


def next_page(driver):
    buttons_menu = driver.find_elements(By.CLASS_NAME, "page-link")
    if not buttons_menu[-1].get_attribute("aria-disabled"):
        ActionChains(driver).click(buttons_menu[-1]).perform()
        return True


def parse_vacancy(vacancy):
    title = vacancy.find_element(By.CLASS_NAME, "job-list-item__link").text
    text = vacancy.find_element(
        By.CSS_SELECTOR,
        "div.job-list-item__description >"
        " span"
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
        "span > "
        "span.mr-2.nobr"
    ).get_attribute("data-original-title")
    views = vacancy.find_element(
        By.CSS_SELECTOR,
        "div.d-flex.align-items-center.font-size-small.mb-2 > "
        "span.job-list-item__counts.d-none.d-lg-inline-block.nobr > "
        "span > "
        "span:nth-child(2) > "
        "span:nth-child(1)"
    ).get_attribute("data-original-title").split(" ")[0]
    applications = vacancy.find_element(
        By.CSS_SELECTOR,
        "div.d-flex.align-items-center.font-size-small.mb-2 > "
        "span.job-list-item__counts.d-none.d-lg-inline-block.nobr > "
        "span > "
        "span:nth-child(2) > "
        "span:nth-child(2)"
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


def parse_all_vacancies(driver):
    all_vacancies_card = driver.find_elements(By.CLASS_NAME, "job-list-item")
    return [parse_vacancy(vacancy) for vacancy in all_vacancies_card]


def get_all_vacancy():
    all_vacancies = []
    with ChromeWebDriver() as driver:
        driver.get(PYTHON_URL)
        all_vacancies.extend(parse_all_vacancies(driver))
        print(f"Page {get_current_page_number(driver)} was parsed!")
        while next_page(driver):
            print(f"Page {get_current_page_number(driver)} was parsed!")
            all_vacancies.extend(parse_all_vacancies(driver))
    export_to_csv(f"123.csv", all_vacancies)


if __name__ == "__main__":
    get_all_vacancy()
