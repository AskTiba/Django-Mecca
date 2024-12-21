import asyncio
import csv
import random
import os
from datetime import datetime
from httpx import ConnectTimeout, Timeout, HTTPStatusError
from twikit import Client

# Constants
QUERY = "from:JadeMwesigwa since:2024-01-01 until:2024-12-20"
COOKIE_FILE = 'cookies.json'
OUTPUT_FILE = 'tweets.csv'
MAX_RETRIES = 5  # Maximum retry attempts for timeouts

async def fetch_tweets_with_retry(client, query, retries=MAX_RETRIES):
    """
    Fetch tweets with retry logic to handle timeouts and HTTP errors.
    """
    for attempt in range(retries):
        try:
            print(f"Fetching tweets for query: '{query}'...")
            return await client.search_tweet(query, product='Top')
        except ConnectTimeout:
            if attempt < retries - 1:
                wait_time = 2 ** attempt + random.uniform(0, 1)
                print(f"Timeout occurred. Retrying in {wait_time:.2f} seconds...")
                await asyncio.sleep(wait_time)
            else:
                print("Max retries reached. Exiting.")
                raise
        except HTTPStatusError as e:
            if e.response.status_code == 429:  # Rate limit error
                wait_time = int(e.response.headers.get("Retry-After", 60))
                print(f"Rate limited. Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                raise

async def login_and_save_cookies(client):
    """
    Handle login and save cookies to a file for future authentication.
    """
    print("Logging in to fetch authentication cookies...")
    await client.login(username="your_username", password="your_password")  # Replace with your credentials
    print("Login successful. Saving cookies to 'cookies.json'.")
    client.save_cookies(COOKIE_FILE)
    print(f"Cookies saved to {COOKIE_FILE}.")

async def fetch_all_tweets(client, query):
    """
    Fetch all tweets for the given query with pagination and sorting.
    """
    all_tweets = []
    tweet_count = 0
    date_format = "%a %b %d %H:%M:%S %z %Y"  # Matches Twitter's created_at format

    # Initial fetch
    tweets = await fetch_tweets_with_retry(client, query)
    if not tweets:
        print("No tweets found for the given query.")
        return all_tweets

    while tweets:
        print(f"Fetched {len(tweets)} tweets in this batch.")
        for tweet in tweets:
            tweet_count += 1
            tweet_data = [
                tweet_count,
                tweet.user.name,
                tweet.text,
                tweet.created_at,
                tweet.retweet_count,
                tweet.favorite_count,
            ]
            all_tweets.append(tweet_data)

        # Attempt to fetch the next batch
        try:
            print("Pagination: Fetching next batch...")
            tweets = await tweets.next()
        except AttributeError:
            print("No more tweets available in pagination.")
            break
        except Exception as e:
            print(f"Error during pagination: {e}")
            break

    print(f"Total tweets fetched: {len(all_tweets)}")
    return all_tweets

async def save_tweets_to_csv(tweets, output_file):
    """
    Save tweets to a CSV file.
    """
    tweets.sort(key=lambda tweet: datetime.strptime(tweet[3], "%a %b %d %H:%M:%S %z %Y"), reverse=True)

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tweet Count', 'Username', 'Text', 'Created_at', 'Retweets', 'Likes'])
        writer.writerows(tweets)

    print(f"Tweets saved to {output_file}.")

async def main():
    """
    Main function to fetch tweets and save them to a CSV file.
    """
    client = Client(language='en-US', timeout=Timeout(30))

    # Check for cookies and authenticate
    if os.path.exists(COOKIE_FILE):
        print("Loading cookies for authentication...")
        client.load_cookies(COOKIE_FILE)
        print("Cookies loaded successfully.")
    else:
        await login_and_save_cookies(client)

    try:
        print(f"Fetching tweets for query: \"{QUERY}\"...")
        all_tweets = await fetch_all_tweets(client, QUERY)

        if all_tweets:
            await save_tweets_to_csv(all_tweets, OUTPUT_FILE)
        else:
            print("No tweets were fetched.")

    except HTTPStatusError as e:
        if e.response.status_code == 429:
            print("Rate limit exceeded. Try again later.")
        else:
            print(f"HTTP Error occurred: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
