# -*- coding: UTF-8 -*-
import json
import csv

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
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


class StdOutListener(StreamListener):
    def on_data(self, data):
        try:
            tweets = json.loads(data)

            with open('..\keys\Data.csv', 'a', encoding='utf-8-sig', newline='') as f:
                w = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

                text = tweets['text']
                link = tweets['id']

                if ('RT' not in text):
                    retweet = False
                else:
                    retweet = True

                user_id = tweets['user']['id_str']
                user_name = tweets['user']['name']
                time = tweets['created_at']
                

                english = translation_en(text)

                if (user_id == '4264276227'):
                    print(time + ' Sentry_Syria validation tweet collected')
                    source = True
                else:
                    print(time + ' Public tweet collected ')
                    source = False

                data = [time, user_id, user_name, text, english, retweet, source, link]
                w.writerow(data)

        except KeyError:
            pass

    def on_error(self, status):
        print(status)

    def heading(*arg):

        with open('..\keys\Data.csv', 'r+', encoding='utf-8-sig', newline='') as f:
            w = csv.reader(f)
            h = csv.writer(f)
            counter = 0
            heading = ['Time', 'User_ID', 'User_Name', 'Text', 'Translation', 'Retweet', 'Source','Tweet_ID']

            for row in w:
                counter += 1

            if (counter < 1):
                print('Inserting new heading')
                h.writerow(heading)
            else:
                print('Appending Data:')

        f.close()


def run_stream(*args):

    alphabet = ['غ', 'ظ', 'ض', 'ذ', 'خ', 'ث', 'ت', 'ش', 'ر', 'ق', 'ص', 'ف', 'ع', 'س', 'ن', 'م', 'ل', 'ك', 'ي', 'ط', 'ح',
                'ز', 'و', 'ه', 'د', 'ج', 'ب']

    words = [' حلب']
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    l = StdOutListener()
    l.heading()

    stream = Stream(auth, l)
    stream.filter(follow=['4264276227'], track=words)

if __name__ == '__main__':
    run_stream()