import tweepy
import pandas as pd
import time
import sys

# Twitter API credentials
client = tweepy.Client(
    consumer_key="HAHftcnVAVQhE4MzJVg0VyN1c",
    consumer_secret="PWgsWa2hXZuEUQm1VLbVp5zAIa5Zlaj6szboUWQMRyuFxNAd9G",
    access_token="1900124331356938240-Zsx6DLimnfxg1JALa5EpGR97k5bAM6",
    access_token_secret="JzcQHawXsdKMcesMWGOa0DX0iADgKmEd5fa1JNJdmycF8",
    wait_on_rate_limit=True
)

# Authenticate with Twitter using OAuth1
auth = tweepy.OAuth1UserHandler(client.consumer_key, client.consumer_secret, client.access_token, client.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Function to scrape tweets
def scrape_tweets(username, num_tweets):
    try:
        tweets = api.user_timeline(screen_name=username, count=num_tweets, tweet_mode="extended")

        attributes_container = [[tweet.created_at, tweet.favorite_count, tweet.source, tweet.full_text] for tweet in tweets]
        columns = ["Date Created", "Number of Likes", "Source of Tweet", "Tweet"]

        # Create a unique filename with timestamp
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{username}_tweets_{timestamp}.csv"
        tweets_df = pd.DataFrame(attributes_container, columns=columns)
        tweets_df.to_csv(filename, index=False) 
        print(f"✅ Scraped {num_tweets} tweets from @{username} and saved to {filename}")

    except tweepy.errors.TweepyException:
        print("⚠️ Rate limit reached. Waiting for reset...")
        time.sleep(15 * 60)  
        scrape_tweets(username, num_tweets) 
    except tweepy.TweepError as e:
        print(f"❌ Tweepy error: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        time.sleep(3)

# Main function to run the scraper
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("⚠️ Usage: python twitter_scarper.py <username> <num_tweets>")
    else:
        username = sys.argv[1]
        num_tweets = int(sys.argv[2])
        scrape_tweets(username, num_tweets)
