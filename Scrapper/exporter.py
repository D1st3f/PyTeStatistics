import csv
import logging
import os
from typing import List

from .scraper import VacancyItem


class CSVExporter:
    @staticmethod
    def export_to_csv(file_name: str, vacancies: List[VacancyItem]) -> None:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.abspath(
            os.path.join(current_directory, os.pardir)
        )
        new_path = os.path.join(parent_directory, "DataCollection", file_name)
        with open(new_path, "w", newline="", encoding="utf-8") as csvfile:
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
        logging.info(f"Saved to '{file_name}' file!")
