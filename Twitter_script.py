# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 01:13:24 2017

@author: Louis
"""
import Twitter_functions as tf
from Twitter_list_object import Twitter_list

api = tf.request_api()
q = 'python jobs'
search = 'search/tweets'
r = api.request(search, {'q': q})

#search = 'statuses/filter'
#r = api.request(search, {'track': q})

#search ='users/show'
#screen_name='StackDevJobs'
#r = api.request(search, {'screen_name': screen_name})

for item in r:
        print(item['text'] if 'text' in item else item)
        if len(item)>1:
            Tweet0 = tf.store_tweet(item,q)
            User0 = tf.store_user(item,q)
            
            if 'tweet_list' not in locals():
                tweet_list = Twitter_list(obj=Tweet0)
            else:
                tweet_list.append(Tweet0)
                
            if 'user_list' not in locals():
                user_list = Twitter_list(obj=User0)
            else:
                user_list.append(User0)


#UserDict = {'user':item['user']['screen_name']}