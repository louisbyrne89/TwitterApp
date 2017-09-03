# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 03:13:22 2017

@author: Louis
"""
from TwitterAPI import TwitterAPI as tw
from Twitter_objects import Tweet, User
import json

def request_api():
    """Twitter API keys loaded from file and API connects to API."""
    with open(r'C:\Users\Louis\python\twitter_not_git\keys.txt', 'r') as f:
        keys = json.load(f)
    api = tw(keys['consumer_key'],
             keys['consumer_secret'],
             keys['access_token'],
             keys['access_token_secret'])
    return api

def store_tweet(item,q):
    """Stores a single tweet in sqlite3 database. Requires two inputs:
            item, which is an object comprising a singe tweet fetched from api.
            q, which is a string for the search terms provided to api."""
            
    hashlst = []
    umlst = []
    url = []
    # 'Hashtag' field reformatted to single string.
    if not item['entities']['hashtags']:  
        [hashlst.append(it['text']) for it in item['entities']['hashtags']]
        hashlst = ','.join(hashlst)   
    # 'User_mentions' field reformatted to single string.
    if not item['entities']['user_mentions']:
        [umlst.append(it['text']) for it in item['entities']['user_mentions']]
        umlst = ','.join(umlst)
    # 'url' field extracted if 'entities' key exists in tweet output.
    if item['entities']['urls']:
        url = item['entities']['urls'][0]['display_url']
    # Important fieds from tweet extracted and saved as new object
    Tweet0 = Tweet(search = q,
                   tweet_id = item['id'],
                   date = item['created_at'],
                   url = url,
                   hashtags = hashlst,
                   user_mentions = umlst,
                   user = item['user']['screen_name'],
                   text = item['text'])
    # Tweet inserted to sqlite3 database
    Tweet0.insert()
    return Tweet0

def store_user(item,q):
    """Stores a single user in sqlite3 database. Requires two inputs:
            item, which is an object comprising a singe tweet fetched from api.
            q, which is a string for the search terms provided to api."""
    # Important fieds from tweet extracted and saved as new object
    User0 = User(search=q,
                 screen_name = item['user']['screen_name'],
                 description = item['user']['description'],
                 user_id = item['user']['id'])
    # User inserted to sqlite3 database
    User0.insert()    
    
    return User0
    
    
    
    