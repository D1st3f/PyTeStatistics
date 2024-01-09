import logging
import os
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

from Scrapper.data_scrapper import get_all_vacancy
from config import TECHNOLOGIES, ORDERED_DAYS

logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)
mlogger = logging.getLogger("matplotlib")
mlogger.setLevel(logging.WARNING)


class DataProcessor:
    def __init__(self):
        self.df = self.read_from_csv()

    @staticmethod
    def create_output_directory(subdirectory):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        output_directory = os.path.join(
            current_directory,
            "..", subdirectory,
            datetime.now().strftime("%Y-%m-%d")
        )
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        return output_directory

    def read_from_csv(self):
        file_name = f'{datetime.now().strftime("Data %Y-%m-%d")}.csv'
        data_collection_directory = os.path.join(
            os.path.dirname(__file__), "..", "DataCollection"
        )
        full_path = os.path.join(data_collection_directory, file_name)

        if os.path.isfile(full_path):
            try:
                logging.info(f"File '{file_name}' found and read!")
                return pd.read_csv(full_path)
            except pd.errors.EmptyDataError:
                logging.error("File is empty! Refreshing data...")
                get_all_vacancy()
                return self.read_from_csv()
        else:
            logging.error("Data file not found! Refreshing data...")
            get_all_vacancy()
            return self.read_from_csv()

    def save_plot(self, figure, output_filename):
        output_directory = self.create_output_directory("DataExport")
        figure.savefig(
            os.path.join(output_directory, output_filename),
            bbox_inches="tight"
        )

    def plot_technology_mentions(self, threshold: int = 5):
        logging.info("Generating 'Technology mentions' plot!")
        tech_mentions = {
            tech: self.df["text"].str.contains(tech, case=False)
            for tech in TECHNOLOGIES
        }
        tech_df = pd.DataFrame(tech_mentions)
        tech_counts = tech_df.sum().reset_index()
        tech_counts.columns = ["Technology", "Mentions"]
        tech_counts = tech_counts[
            tech_counts["Mentions"] > threshold
        ].sort_values(by="Mentions", ascending=False)
        tech_counts["Technology"] = pd.Categorical(
            tech_counts["Technology"].unique(),
            categories=tech_counts["Technology"],
            ordered=True,
        )
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.bar(tech_counts["Technology"],
               tech_counts["Mentions"],
               color="deepskyblue")
        ax.set_title("Mentions of Technologies")
        ax.set_xlabel("Technologies")
        ax.set_ylabel("Number of Mentions")
        ax.tick_params(axis="x", rotation=90)
        plt.tight_layout()

        self.save_plot(fig, "technology_mentions.png")
        plt.close()

    def plot_experience_distribution(self):
        logging.info("Generating 'Experience distribution' plot!")
        experience_df = self.df["experience"].value_counts().reset_index()
        experience_df.columns = ["Experience", "Count"]
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.bar(experience_df["Experience"],
               experience_df["Count"],
               color="lightcoral")
        ax.set_xlabel("Years of Experience")
        ax.set_ylabel("Number of Postings")
        ax.set_title("Distribution Years of Experience")
        plt.tight_layout()
        self.save_plot(fig, "experience_distribution.png")
        plt.close()

    def plot_postings_per_day(self):
        logging.info("Generating 'Postings per day' plot!")
        self.df["created"] = pd.to_datetime(self.df["created"])
        self.df.set_index("created", inplace=True)
        day_of_week_df = self.df.resample("D").size().reset_index()
        day_of_week_df.columns = ["created", "Count"]
        day_of_week_df["Day of Week"] = day_of_week_df["created"].dt.day_name()
        day_of_week_df = (
            day_of_week_df.groupby("Day of Week")["Count"]
            .sum()
            .reindex(ORDERED_DAYS, fill_value=0)
            .reset_index()
        )
        day_of_week_df["Day of Week"] = pd.Categorical(
            day_of_week_df["Day of Week"],
            categories=ORDERED_DAYS,
            ordered=True
        )
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.bar(day_of_week_df["Day of Week"],
               day_of_week_df["Count"],
               color="skyblue")
        ax.set_xlabel("Day of Week")
        ax.set_ylabel("Number of Postings")
        ax.set_title("Number of Postings Added on Each Day of the Week")
        plt.tight_layout()
        self.save_plot(fig, "postings_per_day.png")
        plt.close()

    def plot_combined_image(self) -> None:
        self.plot_technology_mentions()
        self.plot_experience_distribution()
        self.plot_postings_per_day()
        images = [
            "technology_mentions.png",
            "experience_distribution.png",
            "postings_per_day.png",
        ]
        combined_img = plt.figure(figsize=(28, 12))
        for i, img in enumerate(images, 1):
            ax = combined_img.add_subplot(2, 2, i)
            ax.imshow(
                plt.imread(
                    os.path.join(self.create_output_directory("DataExport"),
                                 img)
                )
            )
            ax.axis("off")
        plt.tight_layout()
        self.save_plot(combined_img, "combined_plot.png")
        plt.show()


if __name__ == "__main__":
    data_processor = DataProcessor()
    data_processor.plot_combined_image()
