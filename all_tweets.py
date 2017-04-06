import json
import csv
import tweepy
from tweepy import OAuthHandler
from controller import translation_en

with open("..\keys\some_keys.txt", "r") as key:
    key_list = key.readlines()
    key_list = [i.strip('\n') for i in key_list]
    key.close()


# User credentials. Should not be stored in the code.
access_token = key_list[0]
access_token_secret = key_list[1]
consumer_key = key_list[2]
consumer_secret = key_list[3]

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)



def get_all_tweets():
    all_tweets = []
    new_tweets = tweets = api.user_timeline(screen_name = 'Sentry_Syria', count = 200, include_rts = False)
    all_tweets.extend(new_tweets)
    # save the id of the oldest tweet less one
    oldest = all_tweets[-1].id - 1
    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:

        new_tweets = api.user_timeline(screen_name = 'Sentry_Syria', count = 200, max_id=oldest)
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1
    print("Download Complete\n")


    with open('..\keys\Sentry.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        #heading = ['Time', 'Country', 'Place', 'User_ID', 'User_Name', 'Text', 'Translation', 'Retweet', 'Source']
        #writer.writerow(heading)
        count = 0
        for tweet in all_tweets:

            english = translation_en(tweet.text)
            print("[",count,"]" , " Tweets Translated\n")
            count +=1

            tweets = [tweet.created_at, tweet.user.id, tweet.user.name,tweet.text,english, tweet.retweeted,True]
            writer.writerow(tweets)


if __name__ == '__main__':
    get_all_tweets()


