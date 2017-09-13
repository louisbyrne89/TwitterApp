# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 01:07:55 2017

@author: Louis
"""
from Mediators.mediators import Mediator, Database_connector
from Twitter.Twitter_objects import Twitter_object

class Twitter_list:
    """Twitter list class. Defines a list of twitter objects."""
    def __init__(self,columns=None,data=None,obj=None):
        """Initiates function. If data (2D list of twitter data with columns
        provided as seperate variable) is provided when class is initiated,
        for each row of data one Tweet object is created and stored in the 
        'data' attribute. If a tweet is provided, this is inserted directly
        into list. Otherwise 'data' attribute is empty cell."""
        self.Database_connector = Database_connector
        self.Mediator = Mediator
        self.data = []
        if data and columns:            
            for row in data:
                kwargs = dict([(col, row[i]) for i,col in enumerate(columns)])
                obj = Twitter_object(**kwargs)                
                self.data.append(obj)
        elif obj:
            self.data.append(obj)

    def __len__(self):
        """ returns length of twitter list."""
        return len(self.data)
    
    def __iter__(self):
        """ iterates over twitter_list."""
        yield from self.data
        
    def __getitem__(self, idx):
        """enables indexing of twitter list."""
        return self.data[idx]
    
    def append(self,item):
        """ append one object to twitter list."""
        self.data.append(item)
        
    def pop(self):
        """ get last object of twitter list and remove item from list."""
        item = self.data[-1]
        self.data = self.data[:-1]
        return item
    
    def extend(self,item):
        """ extend twitter list by multiple objects."""
        self.data.extend(item)
        
        
class Tweet_list(Twitter_list):
    def insert(self,tablename='tweets'):
        """Checks required fields present in all tweet objects then inserts
        into 'tweets' table if so.
        """
        for tweet in self.data:
            if not set(['user','text','tweet_id','url','hashtags','date',
                        'user_mentions']) <= set(tweet.fields):
                raise ValueError('All required fields were not provided.')  
        self.Database_connector.insert(self,tablename)
    
    def retrieve(self,tablename='tweets',fields=None,**kwargs):
        """Retrieves data from database using specified fields and keyword
        arguments. See help Database_connector.retrieve for more information.
        """
        self.Database_connector.retrieve(self,tablename,fields,**kwargs)
        
    def process(self,keywords):
        """Returns the percentage of tweets containing a set of keywords.
        """
        if not self.keyword_scores:
            self.keyword_scores = []
        for keyword in keywords:
            score = 0
            for item in self.data:   
                if keyword in item.text.lower():
                    score += 1
                score = score/len(self.data)
            self.keyword_scores[keyword] = score
    
    
class User_list(Twitter_list):
    def insert(self,tablename='users'):
        """Checks required fields present in all user objects then inserts
        into 'users' table if so.
        """
        for user in self.data:
            if (not set(['user_id','screen_name','description']) 
                        <= set(user.fields)):
                raise ValueError('All required fields were not provided.')
        self.Database_connector.insert(self,tablename)
    
    def retrieve(self,tablename='users',fields=None,**kwargs):
        """Retrieves data from database using specified fields and keyword
        arguments. See help Database_connector.retrieve for more information.
        """        
        self.Database_connector.retrieve(self,tablename,fields,**kwargs)
 
