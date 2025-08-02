import pandas as pd
import pyodbc # Pyodbc is a Python library that allows you to connect to Microsoft SQL Server databases using ODBC.
import nltk
from nltk.sentimen.vader import SentimentIntensityAnalyzer

# Download the Vader lexicon for sentiment analysis
nltk.download('vader_lexicon')

def fetch_data_sql():
    connenction_str = (
        "Driver={SQL SERVER};"
        "Server=TINIUS;"
        "Database=PortfolioProject_MarketingAnalystics;"
        "Trusted_Connection = yes;"
    )
    #Establish connection to the SQL database
    conn = pyodbc.connect(connenction_str)
    #Fetch data from the Cstomer review table
    query = "SELECT ReviewID,CustomerID,ProductID,ReviewDate,Rating,ReviewText FROM customer_review"
    df = pd.read_sql(query, conn)
    conn.close()
    #Returning data from the database
    return df

customer_reviews_df = fetch_data_sql()

#Initalize the Vader Sentiment Intensity Analyzer
sia = SentimentIntensityAnalyzer()

def calculate_sentiment(review_text):
    sentiment = sia.polarity_scores(review_text) 
    return sentiment['compound']

def categorize_sentiment(score,rating):
    #Combining the sentiment score and numeric rating give to determine the sentiment category
    if score >= 0.05:
        if rating >= 4:
            return "Positive" #Positive sentiment and high rating
        elif rating == 3:
            return "Mixed Positive" # Positive sentiment and medium rating
        else:
            return "Mixed Negative" #Positive sentiment and low rating
    elif score <= -0.05:
        if rating <= 2:
            return "Negative" #Negative sentiment and low rating
        elif rating == 3:
            return "Mixed Negative" #Negative sentiment and medium rating
        else:
            return "Mixed Positive" #Negative sentiment and high rating
    else:
        return "Neutral" #Neutral sentiment and medium rating
        
