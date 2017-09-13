# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 23:13:47 2017

@author: Louis
"""

class Twitter_object:
    """ Twitter object """
    def __init__(self,**kwargs):
        """ Initiates class. Keyword arguments (twitter fields) stored as class 
        attriubutes. Empty cells stored as empty strings. List of twitter 
        fields which have been retrieved stored as self.fields 
        """
        self.fields = []
        for key,value in kwargs.items():
            if value:
                setattr(self,key,value)
            else:
                setattr(self,key,'')
                
            self.fields.append(key)

    def print_object(self,*args):
        """Prints tweet to screen. Option arguments specifying attributes to
        print to screen are required.
        """
        # stores input fields as dictionary with their value extracted from
        # the twitter object.
        Dict = dict([(att, getattr(self,att)) for att in args])
        # Create print string. format field: value\n. None string types are
        # converted to strings.
        string = ''
        for key,val in Dict.items():
            if not isinstance(val,str):
                val = str(val)
            string = string + '{}: {}\n'.format(key,val)
        return print(string)
        
        
class Tweet(Twitter_object):
    """Tweet subclass"""
    def __init__(self,**kwargs):
        """Initiates class. If any of the fields 'user','text' or 'tweet' 
        are not provided as **kwargs then an error is returned.
        """
        super().__init__(**kwargs)
        if not set(['user','text','tweet_id']) <= set(kwargs.keys()):
            raise KeyError('Either text, user or tweet_id field not ' +
                                  'provided.')
    
    def __str__(self):
        return '{}: {}'.format(self.user, self.text)
 
    
class User(Twitter_object):
    """User_subclass"""
    def __init__(self,**kwargs):
        """Initiates class. If either of the fields 'screen_name' or 'user_id' 
        are not provided as **kwargs then an error is returned.
        """
        super().__init__(**kwargs)
        if (not set(['user_id','screen_name','description']) 
                    <= set(kwargs.keys())):
            raise KeyError('Either user_id or screen_name field not ' +
                                  'provided.')
    
    def __str__(self):
        return '{}: {}'.format(self.screen_name, self.description)
    
    def get_tweets(self,api,count=2000):
        """Retrieves last 'count' tweets from user. Default set to 2000."""
        search = 'statuses/user_timeline'
        api.request(search, {'user_id': self.user_id,
                             'count': count,
                             'exculde_replies':'true',
                             'include rts': 'false'})
       return api