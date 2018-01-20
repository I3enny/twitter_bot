#!/usr/bin/env python3.5

from tweepy import OAuthHandler

import json

from credentials import *

from elasticsearch import Elasticsearch

import tweepy
import time
from time import gmtime

import datetime

def main():
    delta_time = datetime.datetime.now() - datetime.timedelta(days=3)
    index = delta_time.strftime("%Y.%m.%d")
    
    try:
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        
        es = Elasticsearch()
        res = es.search(index=index, doc_type='tweet', size=1000)
            
        tweets = res['hits']['hits']
        
        for tweet in tweets:
            try:
                source = tweet['_source']
                if not source['retweeted']:
                    id_of_tweet = source['id_str']
                    tweet = api.get_status(id_of_tweet)
                    json_data = tweet._json
                    es.index(index='tweet_updated_' + index, doc_type='tweet', body=json_data)
                    print(id_of_tweet)
            except tweepy.RateLimitError as e:
                print(e)
                time.sleep(60 * 15)
            except tweepy.TweepError as e:
                print(e)
            except Exception as e:
                print(e)
                
    except Exception as e:
        print(e)
            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(e)
