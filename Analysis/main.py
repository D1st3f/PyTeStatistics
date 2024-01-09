import logging
import os
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame

from Scrapper.manage import get_all_vacancy
from config import TECHNOLOGIES, ORDERED_DAYS

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)
mlogger = logging.getLogger('matplotlib')
mlogger.setLevel(logging.WARNING)


def read_from_csv() -> DataFrame:
    file_name = f'{datetime.now().strftime("Data %Y-%m-%d")}.csv'
    current_directory = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_directory, "..", "DataCollection",
                             file_name)
    if os.path.isfile(full_path):
        try:
            logging.info(f"File '{file_name}' found and read!")
            return pd.read_csv(full_path)
        except pd.errors.EmptyDataError:
            logging.error("File is empty! Refreshing data...")
            get_all_vacancy()
            return read_from_csv()
    else:
        logging.error("Data file not found! Refreshing data...")
        get_all_vacancy()
        return read_from_csv()


def plot_technology_mentions(data_frame: DataFrame, threshold: int = 5):
    logging.info(f"Generating 'Technology mentions' plot!")
    tech_mentions = {tech: data_frame['text'].str.contains(tech, case=False)
                     for tech in TECHNOLOGIES}
    tech_df = pd.DataFrame(tech_mentions)
    tech_counts = tech_df.sum().reset_index()
    tech_counts.columns = ['Technology', 'Mentions']
    tech_counts = tech_counts[tech_counts['Mentions'] > threshold].sort_values(
        by='Mentions', ascending=False)
    tech_counts['Technology'] = pd.Categorical(
        tech_counts['Technology'].unique(),
        categories=tech_counts['Technology'], ordered=True
    )
    plt.figure(figsize=(15, 6))
    plt.bar(tech_counts['Technology'], tech_counts['Mentions'],
            color='deepskyblue')
    plt.title('Mentions of Technologies')
    plt.xlabel('Technologies')
    plt.ylabel('Number of Mentions')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    logging.info(f"'Technology mentions' plot created!")


def plot_experience_distribution(data_frame: DataFrame):
    logging.info(f"Generating 'Experience distribution' plot!")
    experience_df = data_frame['experience'].value_counts().reset_index()
    experience_df.columns = ['Experience', 'Count']
    plt.figure(figsize=(15, 6))
    plt.bar(experience_df['Experience'], experience_df['Count'],
            color='lightcoral')
    plt.xlabel('Years of Experience')
    plt.ylabel('Number of Postings')
    plt.title('Distribution Years of Experience')
    plt.show()
    logging.info(f"'Experience distribution' plot created!")


def plot_postings_per_day(data_frame: DataFrame):
    logging.info(f"Generating 'Postings per day' plot!")
    data_frame['created'] = pd.to_datetime(df['created'])
    data_frame.set_index('created', inplace=True)
    day_of_week_df = df.resample('D').size().reset_index()
    day_of_week_df.columns = ['created', 'Count']
    day_of_week_df['Day of Week'] = day_of_week_df['created'].dt.day_name()
    day_of_week_df = day_of_week_df.groupby('Day of Week')[
        'Count'].sum().reindex(
        ORDERED_DAYS, fill_value=0
    ).reset_index()
    day_of_week_df['Day of Week'] = pd.Categorical(
        day_of_week_df['Day of Week'], categories=ORDERED_DAYS, ordered=True
    )
    plt.figure(figsize=(15, 6))
    plt.bar(day_of_week_df['Day of Week'],
            day_of_week_df['Count'],
            color='skyblue')
    plt.xlabel('Day of Week')
    plt.ylabel('Number of Postings')
    plt.title('Number of Postings Added on Each Day of the Week')
    plt.show()
    logging.info(f"'Postings per day' plot created!")


df = read_from_csv()
plot_technology_mentions(df)
plot_experience_distribution(df)
plot_postings_per_day(df)
