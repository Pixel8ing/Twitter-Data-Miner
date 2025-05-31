 Twitter Sentiment Analysis Tool
A comprehensive Python tool for scraping Twitter data and performing advanced sentiment analysis with beautiful visualizations.

Features

Dual Sentiment Analysis: Uses both TextBlob and VADER sentiment analyzers
Real-time Data Scraping: Fetches tweets directly from Twitter API
Comprehensive Data Export: Saves detailed CSV files with all metrics
Beautiful Visualizations: Generates professional charts and graphs
Text Preprocessing: Cleans tweets for better analysis accuracy
Rate Limit Handling: Automatically manages Twitter API rate limits
Progress Tracking: Real-time progress updates during analysis

 Analysis Methods
TextBlob Analysis

Polarity: Measures sentiment from -1 (negative) to +1 (positive)
Subjectivity: Measures objectivity from 0 (objective) to 1 (subjective)

VADER Analysis

Compound Score: Overall sentiment intensity from -1 to +1
Detailed Breakdown: Positive, neutral, and negative sentiment percentages
Social Media Optimized: Specially designed for informal text analysis

 Quick Start
Prerequisites
bashpip install tweepy pandas textblob vaderSentiment matplotlib seaborn
Twitter API Setup

Create a Twitter Developer account at developer.twitter.com
Create a new app and generate API keys
Replace the placeholder credentials in the code:

pythonclient = tweepy.Client(
    consumer_key="YOUR_CONSUMER_KEY",
    consumer_secret="YOUR_CONSUMER_SECRET",
    access_token="YOUR_ACCESS_TOKEN",
    access_token_secret="YOUR_ACCESS_TOKEN_SECRET",
    wait_on_rate_limit=True
)

Usage

bashpython twitter_sentiment_scraper.py <username> <number_of_tweets>

Examples:
bashpython twitter_sentiment_scraper.py elonmusk 50
python twitter_sentiment_scraper.py taylorswift13 100
python twitter_sentiment_scraper.py nasa 25

Output Files
1. CSV Data File
Contains comprehensive tweet data with sentiment metrics:

Basic tweet information (date, likes, source, text)
Cleaned text for analysis
TextBlob sentiment scores
VADER sentiment scores
Detailed sentiment breakdowns

2. Visualization File
Professional charts including:

Sentiment Distribution Pie Charts (TextBlob & VADER)
Sentiment Trends Over Time
Polarity vs Subjectivity Scatter Plot
Engagement Analysis

3. Console Summary
Real-time statistics including:

Sentiment distribution percentages
Average sentiment scores
Most positive/negative tweets
Processing progress
