import pandas as pd
import pyodbc # Pyodbc is a Python library that allows you to connect to Microsoft SQL Server databases using ODBC.
import nltk
from nltk.sentimen.vader import SentimentIntensityAnalyzer

# Download the Vader lexicon for sentiment analysis
nltk.download('vader_lexicon')

def fetch_data_sql():
    