import logging
import os
from datetime import datetime

import pandas as pd

from Scrapper.manage import get_all_vacancy

logging.basicConfig(format='%(levelname)s - %(message)s',
                    level=logging.INFO)


def read_from_csv():
    file_name = f'{datetime.now().strftime("Data %Y-%m-%d")}.csv'
    current_directory = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_directory,
                             "..",
                             "DataCollection",
                             file_name)
    if os.path.isfile(full_path):
        try:
            df = pd.read_csv(full_path)
            print(df.head())
        except pd.errors.EmptyDataError:
            logging.error("File is empty!")
            get_all_vacancy()
    else:
        logging.error("Need refresh data!")
        get_all_vacancy()


read_from_csv()
