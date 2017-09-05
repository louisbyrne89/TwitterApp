# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 01:13:24 2017

@author: Louis
"""
import Twitter.Twitter_functions as tf
from Database.database_objects import Tweet_list_db, User_list_db



api = tf.request_api()
search = 'search/tweets'
indict = {'q': 'python jobs',
          'lang':'en'}

req = api.request(search, indict)
#req = tf.get_tweets(api,q)

a=0
for item in req:
        a+=1
        print(item['text'] if 'text' in item else item)
        if len(item)>1:
            Tweet0 = tf.create_tweet_object(item)
            User0 = tf.create_user_object(item)
            
            if 'tweet_list' not in locals():
                tweet_list = Tweet_list_db(obj=Tweet0)
            else:
                tweet_list.append(Tweet0)
                
            if 'user_list' not in locals():
                user_list = User_list_db(obj=User0)
            else:
                user_list.append(User0)

len(req.response.json()['statuses'])