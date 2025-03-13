Twitter Data Scraper
A Python-based Twitter scraper using Tweepy that extracts tweets from a specific user and saves them in a CSV file.

Features
Scrapes recent tweets from a Twitter user.
Saves tweets in a structured CSV format.
Includes error handling and rate-limit management.
Supports command-line arguments for username and tweet count.

Clone this repository:
git clone https://github.com/yourusername/twitter-data-scraper.git
cd twitter-data-scraper

Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
pip install tweepy pandas

Setup Twitter API Keys
To use this scraper, you need to set up a Twitter Developer Account and create an application to get API keys.

Go to Twitter Developer Portal.
Create an App and generate:
API Key
API Secret Key
Access Token
Access Token Secret
Update twitter_scraper.py with your credentials.

Run the script in the terminal:

python twitter_scraper.py <username> <num_tweets>
Example:

python twitter_scraper.py elonmusk 25

(This will scrape 25 tweets from @elonmusk and save them to a CSV file.)

Common Issues & Fixes
401 Unauthorized (Authentication Error)
  Check if your API keys are correct.
  Ensure your Twitter Developer App has read permissions.
  
Rate Limit Reached
  Twitter restricts API calls; the script waits for 15 minutes if needed.
  Try again after some time.
  
ModuleNotFoundError: No module named ‘tweepy’
  Run pip install tweepy pandas again.
  
To-Do List
   Add support for scraping tweets using hashtags.
   Implement sentiment analysis on tweets.
   Store data in a database instead of CSV.
