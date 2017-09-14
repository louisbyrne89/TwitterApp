# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 20:32:14 2017

@author: Louis
"""

def get_user_tweets(mediator,user,count=2000):
    """Retrieves last 'count' tweets from user. Default set to 2000.
    Inputs:
        mediator: mediator instance
        user: user instance.
    """
    search = 'statuses/user_timeline'
    mediator.Api_control.request(search, {'user_id': user.user_id,
                                           'count': count,
                                           'exculde_replies':'true',
                                           'include rts': 'false'})
    return mediator.create_tweet_list()

def sample_tweets(mediator,search,indict):   
    """Samples latest tweets for keyword list.
    Inputs:
        mediator: mediator instance
        search: twitter feature to search
        indict: keywords to search
    """
    mediator.Api_control.request(search,indict)
    return mediator.create_tweet_list(), mediator.create_user_list()
        
        
#    def get_followers():
#        
#    def get_following():