from microsofttranslator import Translator
import pandas
import os
from threading import Thread
import time

with open("..\keys\some_keys.txt", "r") as key:
    key_list = key.readlines()
    key_list = [i.strip('\n') for i in key_list]
    translate = Translator(key_list[4], key_list[5])
    key.close()

def translation_ar(x):
    return translate.translate(x,'ar')

def translation_en(x):
    return translate.translate(x,'en')

def remove_place(*args):
    dfr = pandas.read_csv('..\keys\Data.csv')
    keep_cols = ['Time', 'User_ID', 'User_Name', 'Text', 'Translation', 'Retweet', 'Source']
    new_dfr = dfr[keep_cols]
    new_dfr.to_csv("..\keys\Data.csv", index=False,encoding='utf-8')

def run_stream():
    while(1):
        os.system("python twit_stream.py")

def run_analysis():
    while(1):
        time.sleep(60)
        os.system("python analysis.py")

if __name__ == '__main__':
    Thread(target = run_stream).start()
    Thread(target = run_analysis).start()



