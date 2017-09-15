# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 20:43:33 2017

@author: Louis
"""
import Twitter.Twitter_functions as tf
from Twitter.Twitter_objects import Tweet_list, User_list

from Mediator.mediator import Control

# Load mediator
ctrl = Control()


# Search twitter for keywords
search = 'search/tweets'
indict = {'q': 'jobs python junior',
          'lang':'en'}
tweet_list, user_list = tf.sample_tweets(ctrl,search,indict)

# search twitter stream for keywords
#search = 'statuses/filter'
#indict = {'q': 'trump',
#          'lang':'en'}
#tweet_list,users = ctrl.sample_tweets(search,indict)

# insert users and tweets into database
#tweet_list.insert()

user_list.insert()

# Get all tweets (id, text and user) from database with a tweet_id > 100 whose 
# username isnt 'louisbyrne'
tweet_list = Tweet_list()
tweet_list.set_mediator(ctrl)
tweet_list.retrieve(fields=['tweet_id','text','user'],tweet_id='>100',
                    user='!= "louisbyrne"')

# get users follwers list
user = user_list[0]
#user_list = tf.get_followers(ctrl, user)

# process twitter users for keywords.
keywords = ['python','sql','junior','flexi',
                'remote','london','uk','bristol']
tf.process_tweets(ctrl, keywords)



    

