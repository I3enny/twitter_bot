#!/usr/bin/env python3.5

from credentials import *

from datetime import datetime
from elasticsearch import Elasticsearch

# from time import gmtime, strftime

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

class StdOutListener(StreamListener):
    def __init__(self):
        self.es = Elasticsearch()
        
    def on_data(self, data):
        print(data)
        self.es.index(index=data[0], doc_type='tweet', body=data)
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
    main()
