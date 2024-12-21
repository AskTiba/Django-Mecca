import asyncio
import csv
import random
from datetime import datetime
from httpx import ConnectTimeout, Timeout, HTTPStatusError
from twikit import Client

# Constants
QUERY = "chatgpt"  # Replace with your search query
MIN_TWEETS = 100  # Minimum number of tweets to fetch
COOKIE_FILE = 'cookies.json'
OUTPUT_FILE = 'tweets.csv'
MAX_RETRIES = 5  # Maximum retry attempts for timeouts


async def fetch_tweets_with_retry(client, query, retries=MAX_RETRIES):
    """
    Fetch tweets with retry logic to handle timeouts and HTTP errors.
    """
    for attempt in range(retries):
        try:
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
                raise


async def main():
    """
    Main function to fetch tweets and save them to a CSV file.
    """
    # Initialize the client with a higher timeout
    client = Client(language='en-US', timeout=Timeout(30))
    client.load_cookies(COOKIE_FILE)
    print("Login successful and cookies loaded.")

    tweet_count = 0
    all_tweets = []

    try:
        print(f'{datetime.now()} - Fetching tweets...')
        tweets = await fetch_tweets_with_retry(client, QUERY)

        while tweet_count < MIN_TWEETS:
            if not tweets:
                print(f'{datetime.now()} - No more tweets found.')
                break

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

                if tweet_count >= MIN_TWEETS:
                    break

            # Random delay between requests to avoid rate limits
            await asyncio.sleep(random.uniform(5, 15))
            tweets = await tweets.next()

        # Save tweets to CSV
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['tweet_count', 'Username', 'Text', 'Created_at', 'Retweets', 'Likes'])
            writer.writerows(all_tweets)

        print(f'{datetime.now()} - Done! Saved {tweet_count} tweets to {OUTPUT_FILE}.')

    except HTTPStatusError as e:
        if e.response.status_code == 429:
            print(f'{datetime.now()} - Rate limit exceeded. Try again later.')
        else:
            print(f'{datetime.now()} - HTTP Error occurred: {e.response.status_code} - {e.response.text}')
    except Exception as e:
        print(f'{datetime.now()} - An error occurred: {e}')
        import traceback
        traceback.print_exc()


# Entry point
if __name__ == "__main__":
    asyncio.run(main())
