# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 00:30:24 2017

@author: Louis
"""
from Twitter.Twitter_objects import Tweet_list, User_list
from Twitter.API import Api_control
import Twitter.API

class Control:
    """This class controls the interactions between the API, tweet and user
    classes.
    """
    def __init__(self):
        """Initialises class"""
        self.Tweet_list = Tweet_list
        self.User_list = User_list
        self.Api_control = Api_control()
    
    def create_tweet_list(self):
        """Create a tweet list by looping through API request."""
        Tweet_list = self.Tweet_list(self)
        for item in self.Api_control.req:
            print(item['text'] if 'text' in item else item)
            if len(item)>1:
                # Create tweet and user instances
                Tweet_list.append(item)
        return Tweet_list
    
    def create_user_list(self):
        """Create a user list by looping through API request."""
        User_list = self.User_list(self)
        for item in self.Api_control.req:
            print(item['text'] if 'text' in item else item)
            if len(item)>1:
                # Create tweet and user instances
                User_list.append(item)
        return User_list

    
                        
    