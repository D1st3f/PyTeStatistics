# PyTeStatistics

#### This project was created for data scraping and data analysis of Python developer jobs on the site [djinni.co](https://djinni.co/jobs/?primary_keyword=Python). It builds graphs for detailed study and data analysis.

## 👩‍💻 _Installation & Run_
### 🧠 Set up the environment 

 On Windows:
```python
python -m venv venv 
venv\Scripts\activate
 ```

 On macOS:
```python
python3 -m venv venv 
source venv/bin/activate
 ```

### 👯 Set up requirements 
```python
pip install -r requirements.txt
```

### 👩‍ Set up [config.py](config.py) 
You can change that file to reorder days of week or change what technologies you want to count.


## 🍈 _How that works..._
### 🧠 Scrapping:
- You can run ```python .\Scrapper\data_scrapper.py``` to start process.
- Now you will get a new **.csv** database in [DataCollection](DataCollection) folder.
### 😋 Work with data:
- You can run ```python .\Analysis\data_processor.py``` to start process. It will check if database exists, if not will start scrapping.
- In [DataCollection](DataCollection) folder you will get folder with current date, inside will be plots.
- All diagrams will be compiled to single one - **combined_plot.png**.
![combined_plot.png](DataExport%2F2024-01-09%2Fcombined_plot.png)
- And there will be separate diagrams.
![experience_distribution.png](DataExport%2F2024-01-09%2Fexperience_distribution.png)
![location_distribution.png](DataExport%2F2024-01-09%2Flocation_distribution.png)
![postings_per_day.png](DataExport%2F2024-01-09%2Fpostings_per_day.png)
![technology_mentions.png](DataExport%2F2024-01-09%2Ftechnology_mentions.png)

# 😋 GL HF!