#!/usr/bin/env python3.5

from credentials import *

import json
import time

from elasticsearch import Elasticsearch

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

class StdOutListener(StreamListener):
    def __init__(self):
        self.es = Elasticsearch()
        
    def on_data(self, data):
        # print(data)
        json_data = json.loads(data)
        print(json_data)
        self.es.index(index=time.strftime("%Y.%m.%d"), doc_type='tweet', body=json_data)
        return True

    def on_error(self, status):
        print('Error : ' + str(status))


def main():
    keywords = ['#cyberattaque', '#cybersecurite', '#cyberdefense', '#FIC2018']

    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, l)

    stream.filter(track=keywords)
    
if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(e)
