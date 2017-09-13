# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 20:43:33 2017

@author: Louis
"""
import Twitter.Twitter_functions as tf
from Twitter.Twitter_lists import Tweet_list, User_list
from Mediators.mediators import Api_control

# Connect to api
api = Api_control()


# search twitter for keywords
search = 'search/tweets'
indict = {'q': 'python jobs',
          'lang':'en'}
req = api.api.request(search, indict)
tweet_list, user_list = tf.sampling(api.api,search,indict)

# search twitter stream for keywords
search = 'statuses/filter'
indict = {'q': 'python jobs',
          'lang':'en'}
#req = api.request(search, indict)
#tweet_list, user_list = tf.sampling(api,search,indict)

# insert users and tweets into database
tweet_list.insert()
user_list.insert()

# Get all tweets (id, text and user) from database with a tweet_id > 100 whose 
# username isnt 'louisbyrne'

tweet_list = Tweet_list()
tweet_list.retrieve(fields=['tweet_id','text','user'],tweet_id='>100',
                    user='!= "louisbyrne"')


    

