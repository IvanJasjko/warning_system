# -*- coding: UTF-8 -*-

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import csv
# from yandex_translate import YandexTranslate
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


# List of attributes available in JSON string



class StdOutListener(StreamListener):
    def on_data(self, data):

        tweets = json.loads(data)

        with open('..\keys\Data.csv', 'a', encoding='utf-8-sig', newline='') as f:
            w = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)

            text = tweets['text']

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

            data = [time, user_id, user_name, text, english, retweet, source]
            w.writerow(data)

    def on_error(self, status):
        print(status)

    def heading(*arg):

        with open('..\keys\Data.csv', 'r+', encoding='utf-8-sig', newline='') as f:
            w = csv.reader(f)
            h = csv.writer(f)
            counter = 0
            heading = ['Time', 'User_ID', 'User_Name', 'Text', 'Translation', 'Retweet', 'Source']

            for row in w:
                counter += 1

            if (counter < 1):
                print('Inserting new heading')
                h.writerow(heading)
            else:
                print('Appending Data:')

        f.close()


if __name__ == '__main__':


    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    l.heading()
    alphabet = ['غ', 'ظ', 'ض', 'ذ', 'خ', 'ث', 'ت', 'ش', 'ر', 'ق', 'ص', 'ف', 'ع', 'س', 'ن', 'م', 'ل', 'ك', 'ي', 'ط', 'ح',
                'ز', 'و', 'ه', 'د', 'ج', 'ب']

    words = [ ' حلب']

    stream.filter(follow=['4264276227'], track=words) #, "788821589496303624"
