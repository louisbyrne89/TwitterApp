# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 00:30:24 2017

@author: Louis
"""
from Twitter.Twitter_objects import Tweet_list, User_list
from Twitter.API import Api_control, Database_connector
import Twitter.API

class Control:
    """This class controls the interactions between the API, tweet and user
    classes.
    """
    def __init__(self):
        """Initialises class"""
        self._tweet_list = Tweet_list
        self._user_list = User_list
        self._api_control = Api_control()
        self._database_connector = Database_connector
       
    def create_tweet_list(self, req,p2s=False):
        """Create a tweet list by looping through API request."""
        Tweet_list = self._tweet_list()
        Tweet_list.set_mediator(self)
        for item in req:
            if p2s:
                print(item['text'] if 'text' in item else item)
            if len(item) > 1:
                # Create tweet instance
                Tweet_list.cappend(item)
        return Tweet_list
    
    def create_user_list(self, req, p2s = False, obj = 'tweet'):
        """Create a user list by looping through API request."""
        User_list = self._user_list()
        User_list.set_mediator(self)
        for item in req:
            if p2s:
                print(item['text'] if 'text' in item else item)
            if len(item) > 1:
                #import pdb; pdb.set_trace()
                # Create user instance
                if obj == 'tweet':
                    screen_name = item['user']['screen_name']
                    description = item['user']['description']
                    user_id = item['user']['id']
                    followings = item['user']['friends_count']
                    followers = item['user']['followers_count']
                    
                elif obj == 'user':
                    screen_name = item['screen_name']
                    user_id = item['id']
                    description = item['description']
                    followings = item['friends_count']
                    followers = item['followers_count']
                
                User_list.cappend(screen_name = screen_name,
                                      description = description,
                                      user_id = user_id,
                                      followings = followings,
                                      followers = followers)                                      
        return User_list

    
                        
    