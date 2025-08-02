import pandas as pd
import pyodbc # Pyodbc is a Python library that allows you to connect to Microsoft SQL Server databases using ODBC.
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the Vader lexicon for sentiment analysis
#nltk.download('vader_lexicon') #Only needed if not preinstalled 


def fetch_data_sql():
    connenction_str = (
        #Establish the string for connecting to my databse
        "Driver={ODBC Driver 17 for SQL Server};"  
         #Redacted as database is deleted after this csv pull, will add .bak file to project
        "Server=XX" 
        "Database=XX;"  
        "Trusted_Connection=yes;"
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
        if rating > 4:
            return "Positive" # Postivite rating and neutral sentiment
        elif rating <= 2:
            return "Negative" #Negative rating and netural sentiment score
        else:
            return "Neutral" #Neutral rating and sentiment

#Bucket to score sentiment into ranges 
def sentiment_buckets(score):
    if score >= 0.5:
        return "0.5 to 1.0"
    elif 0.0   <= score <0.5:
        return "0.0 to 0.49"
    elif -0.5 <= score <0.0:
        return "-0.5 to 0.0"
    else:
        return "-1.0 to -0.5" 

#Apply sentiment analysis to calculate the sentiment scores for each review, categorization and apply bucketing to defined ranges 
customer_reviews_df['SentimentScore'] = customer_reviews_df['ReviewText'].apply(calculate_sentiment)
customer_reviews_df['SentimentCategory'] = customer_reviews_df.apply(
    lambda row: categorize_sentiment(row['SentimentScore'],row['Rating']), axis = 1)
     
customer_reviews_df['SentimentBucket'] = customer_reviews_df['SentimentScore'].apply(sentiment_buckets)

print(customer_reviews_df.head())
#Save the dataframe to a .csv file
customer_reviews_df.to_csv('customer_review_with_sentiment.csv',index = False) 
