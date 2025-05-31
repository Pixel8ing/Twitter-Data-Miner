import tweepy
import pandas as pd
import time
import sys
import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

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

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

def clean_tweet(tweet_text):
    """Clean tweet text for better sentiment analysis"""
    # Remove URLs, mentions, hashtags, and special characters
    tweet_text = re.sub(r'http\S+|www\S+|https\S+', '', tweet_text, flags=re.MULTILINE)
    tweet_text = re.sub(r'@\w+|#\w+', '', tweet_text)
    tweet_text = re.sub(r'[^\w\s]', '', tweet_text)
    return tweet_text.strip()

def get_textblob_sentiment(text):
    """Get sentiment using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.1:
        sentiment = 'Positive'
    elif polarity < -0.1:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    
    return sentiment, polarity, subjectivity

def get_vader_sentiment(text):
    """Get sentiment using VADER"""
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= 0.05:
        sentiment = 'Positive'
    elif compound <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    
    return sentiment, compound, scores['pos'], scores['neu'], scores['neg']

def analyze_sentiment(tweet_text):
    """Perform comprehensive sentiment analysis"""
    cleaned_text = clean_tweet(tweet_text)
    
    # TextBlob analysis
    tb_sentiment, tb_polarity, tb_subjectivity = get_textblob_sentiment(cleaned_text)
    
    # VADER analysis
    vader_sentiment, vader_compound, vader_pos, vader_neu, vader_neg = get_vader_sentiment(cleaned_text)
    
    return {
        'cleaned_text': cleaned_text,
        'textblob_sentiment': tb_sentiment,
        'textblob_polarity': tb_polarity,
        'textblob_subjectivity': tb_subjectivity,
        'vader_sentiment': vader_sentiment,
        'vader_compound': vader_compound,
        'vader_positive': vader_pos,
        'vader_neutral': vader_neu,
        'vader_negative': vader_neg
    }

def create_sentiment_visualizations(df, username):
    """Create sentiment analysis visualizations"""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    
    # Set up the plotting style
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle(f'Sentiment Analysis for @{username}', fontsize=16, fontweight='bold')
    
    # 1. TextBlob Sentiment Distribution
    textblob_counts = df['TextBlob_Sentiment'].value_counts()
    colors = ['#2ecc71', '#e74c3c', '#f39c12']  # Green, Red, Orange
    axes[0, 0].pie(textblob_counts.values, labels=textblob_counts.index, autopct='%1.1f%%', 
                   colors=colors, startangle=90)
    axes[0, 0].set_title('TextBlob Sentiment Distribution')
    
    # 2. VADER Sentiment Distribution
    vader_counts = df['VADER_Sentiment'].value_counts()
    axes[0, 1].pie(vader_counts.values, labels=vader_counts.index, autopct='%1.1f%%', 
                   colors=colors, startangle=90)
    axes[0, 1].set_title('VADER Sentiment Distribution')
    
    # 3. Sentiment over Time
    df['Date_Created'] = pd.to_datetime(df['Date_Created'])
    df_sorted = df.sort_values('Date_Created')
    
    # Map sentiments to numbers for plotting
    sentiment_map = {'Positive': 1, 'Neutral': 0, 'Negative': -1}
    df_sorted['TextBlob_Score'] = df_sorted['TextBlob_Sentiment'].map(sentiment_map)
    df_sorted['VADER_Score'] = df_sorted['VADER_Sentiment'].map(sentiment_map)
    
    axes[1, 0].plot(range(len(df_sorted)), df_sorted['TextBlob_Score'], 
                    marker='o', label='TextBlob', alpha=0.7)
    axes[1, 0].plot(range(len(df_sorted)), df_sorted['VADER_Score'], 
                    marker='s', label='VADER', alpha=0.7)
    axes[1, 0].set_title('Sentiment Trends Over Tweets')
    axes[1, 0].set_xlabel('Tweet Index (Chronological)')
    axes[1, 0].set_ylabel('Sentiment Score')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Polarity vs Subjectivity Scatter Plot
    scatter = axes[1, 1].scatter(df['TextBlob_Polarity'], df['TextBlob_Subjectivity'], 
                                c=df['Number_of_Likes'], cmap='viridis', alpha=0.6)
    axes[1, 1].set_xlabel('Polarity (Negative ← → Positive)')
    axes[1, 1].set_ylabel('Subjectivity (Objective ← → Subjective)')
    axes[1, 1].set_title('Polarity vs Subjectivity (Color = Likes)')
    plt.colorbar(scatter, ax=axes[1, 1], label='Number of Likes')
    
    plt.tight_layout()
    plot_filename = f"{username}_sentiment_analysis_{timestamp}.png"
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"📊 Sentiment visualization saved as {plot_filename}")

def print_sentiment_summary(df, username):
    """Print summary statistics of sentiment analysis"""
    print(f"\n🔍 SENTIMENT ANALYSIS SUMMARY for @{username}")
    print("=" * 50)
    
    # TextBlob Summary
    print("\n📈 TextBlob Analysis:")
    tb_counts = df['TextBlob_Sentiment'].value_counts()
    for sentiment, count in tb_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {sentiment}: {count} tweets ({percentage:.1f}%)")
    
    print(f"  Average Polarity: {df['TextBlob_Polarity'].mean():.3f}")
    print(f"  Average Subjectivity: {df['TextBlob_Subjectivity'].mean():.3f}")
    
    # VADER Summary
    print("\n📊 VADER Analysis:")
    vader_counts = df['VADER_Sentiment'].value_counts()
    for sentiment, count in vader_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {sentiment}: {count} tweets ({percentage:.1f}%)")
    
    print(f"  Average Compound Score: {df['VADER_Compound'].mean():.3f}")
    
    # Most positive and negative tweets
    print("\n🌟 Most Positive Tweet (TextBlob):")
    most_positive = df.loc[df['TextBlob_Polarity'].idxmax()]
    print(f"  Polarity: {most_positive['TextBlob_Polarity']:.3f}")
    print(f"  Tweet: {most_positive['Tweet'][:100]}...")
    
    print("\n💔 Most Negative Tweet (TextBlob):")
    most_negative = df.loc[df['TextBlob_Polarity'].idxmin()]
    print(f"  Polarity: {most_negative['TextBlob_Polarity']:.3f}")
    print(f"  Tweet: {most_negative['Tweet'][:100]}...")

# Function to scrape tweets with sentiment analysis
def scrape_tweets(username, num_tweets):
    try:
        print(f"🔍 Scraping {num_tweets} tweets from @{username}...")
        tweets = api.user_timeline(screen_name=username, count=num_tweets, tweet_mode="extended")
        
        print("🧠 Analyzing sentiment...")
        tweet_data = []
        
        for i, tweet in enumerate(tweets):
            print(f"  Processing tweet {i+1}/{len(tweets)}", end='\r')
            
            # Basic tweet data
            basic_data = [
                tweet.created_at,
                tweet.favorite_count,
                tweet.source,
                tweet.full_text
            ]
            
            # Sentiment analysis
            sentiment_data = analyze_sentiment(tweet.full_text)
            
            # Combine all data
            row_data = basic_data + [
                sentiment_data['cleaned_text'],
                sentiment_data['textblob_sentiment'],
                sentiment_data['textblob_polarity'],
                sentiment_data['textblob_subjectivity'],
                sentiment_data['vader_sentiment'],
                sentiment_data['vader_compound'],
                sentiment_data['vader_positive'],
                sentiment_data['vader_neutral'],
                sentiment_data['vader_negative']
            ]
            
            tweet_data.append(row_data)
        
        # Define columns
        columns = [
            "Date_Created", "Number_of_Likes", "Source_of_Tweet", "Tweet",
            "Cleaned_Text", "TextBlob_Sentiment", "TextBlob_Polarity", "TextBlob_Subjectivity",
            "VADER_Sentiment", "VADER_Compound", "VADER_Positive", "VADER_Neutral", "VADER_Negative"
        ]
        
        # Create DataFrame
        tweets_df = pd.DataFrame(tweet_data, columns=columns)
        
        # Save to CSV
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{username}_tweets_with_sentiment_{timestamp}.csv"
        tweets_df.to_csv(filename, index=False)
        
        print(f"\n✅ Scraped and analyzed {len(tweets)} tweets from @{username}")
        print(f"💾 Data saved to {filename}")
        
        # Print sentiment summary
        print_sentiment_summary(tweets_df, username)
        
        # Create visualizations
        create_sentiment_visualizations(tweets_df, username)
        
    except tweepy.errors.TweepyException as e:
        print(f"⚠️ Tweepy error: {str(e)}")
        if "rate limit" in str(e).lower():
            print("Rate limit reached. Waiting for reset...")
            time.sleep(15 * 60)
            scrape_tweets(username, num_tweets)
    except tweepy.TweepError as e:
        print(f"⚠️ Legacy Tweepy error: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        time.sleep(3)

# Main function to run the scraper
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("⚠️ Usage: python twitter_sentiment_scraper.py <username> <num_tweets>")
        print("📋 Example: python twitter_sentiment_scraper.py elonmusk 50")
    else:
        username = sys.argv[1]
        num_tweets = int(sys.argv[2])
        
        print("🚀 Starting Twitter Sentiment Analysis...")
        print(f"👤 Target: @{username}")
        print(f"📊 Tweets to analyze: {num_tweets}")
        print("-" * 50)
        
        scrape_tweets(username, num_tweets)
