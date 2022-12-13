from dotenv import dotenv_values
from auth import handle_auth, create_api
from utils import get_handles
from datetime import datetime, timezone, timedelta

import tweepy

def load_dotenv():
    env = dotenv_values('.env')

    try:
        consumer_key = env['TWITTER_CONSUMER_KEY']
        consumer_secret = env['TWITTER_CONSUMER_SECRET']
        bearer_token = env['BEARER_TOKEN']
    except KeyError:
        print(KeyError)
        exit()

    try:
        access_token = env['ACCESS_TOKEN']
        access_token_secret = env['ACCESS_TOKEN_SECRET']
    except KeyError:
        print('Access token info does not exist in the dotenv file')
        access = handle_auth(consumer_key, consumer_secret)
        (access_token, access_token_secret) = access
    
    return (consumer_key, consumer_secret, bearer_token, 
    access_token, access_token_secret)

def main():
    # Load dotenv
    (consumer_key, consumer_secret, bearer_token, 
    access_token, access_token_secret) = load_dotenv()

    # Auth and get api instance
    api = create_api(consumer_key, consumer_secret, access_token, access_token_secret)
    twitter_handles = get_handles()
    users = api.lookup_users(screen_name = twitter_handles)

    # client
    client = tweepy.Client(bearer_token)

    # Get ids from handle
    ids = [user.id for user in users]
    date_now = datetime.now(timezone.utc)
    one_day_before = date_now - timedelta(days=1)

    tweet_ids = []
    for id in ids:
        response = client.get_users_tweets(id = id, exclude=['retweets', 'replies'], 
                                            start_time=one_day_before, tweet_fields=['created_at'],
                                            media_fields=['media_key'], expansions=['attachments.media_keys'])
        
        if response.data is None:
            # no latest tweets from this user, skip
            continue

        for tweet in response.data:
            tweet_ids.append(tweet.id)

    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )
    response = client.create_tweet(
        text='This is a test quote. Beep boop~~',
        quote_tweet_id= tweet_ids[0]
    )
    print(f"https://twitter.com/user/status/{response.data['id']}")

if __name__ == "__main__":
    main()