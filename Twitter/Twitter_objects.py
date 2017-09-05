# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 23:13:47 2017

@author: Louis
"""

class Twitter_object:
    """ Twitter object """
    def __init__(self,**kwargs):
        """ initiates class. Keyword arguments (twitter fields) stored as class 
        attriubutes. Empty cells stored as empty strings. List of twitter 
        fields which have been retrieved stored as self.fields """
        self.fields = []
        for key,value in kwargs.items():
            if value:
                setattr(self,key,value)
            else:
                setattr(self,key,'')
                
            self.fields.append(key)

    def print_object(self,*args):
        """Prints tweet to screen. Option arguments specifying attributes to
        print to screen are required."""
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
        are not provided then an error is returned."""
        super().__init__(**kwargs)
        if not set(['user','text','tweet_id']) <= set(kwargs.keys()):
            raise FieldError('Either text, user or tweet_id field not ' +
                                  'provided.')
    
    def __str__(self):
        return '{}: {}'.format(self.user, self.text)
    
class User(Twitter_object):
    """User_subclass"""
    def __init__(self,**kwargs):
        """Initiates class. If either of the fields 'screen_name' or 'user_id' 
        are not provided then an error is returned."""
        super().__init__(**kwargs)
        if (not set(['user_id','screen_name','description']) 
                    <= set(kwargs.keys())):
            raise FieldError('Either user_id or screen_name field not ' +
                                  'provided.')
    
    def __str__(self):
        return '{}: {}'.format(self.screen_name, self.description)
    
class Twitter_list:
    """Twitter list class. Defines a list of twitter objects"""
    def __init__(self,columns=None,data=None,obj=None):
        """Initiates function. If data (2D list of twitter data with columns
        provided as seperate variable) is provided when class is initiated,
        for each row of data one Tweet object is created and stored in the 
        'data' attribute. If a tweet is provided, this is inserted directly
        into list. Otherwise 'data' attribute is empty cell."""
        self.data = []
        if data and columns:            
            for row in data:
                kwargs = dict([(col, row[i]) for i,col in enumerate(columns)])
                obj = Twitter_object(**kwargs)                
                self.data.append(obj)
        elif obj:
            self.data.append(obj)

    def __len__(self):
        """ returns length of twitter list"""
        return len(self.data)
    
    def __iter__(self):
        """ iterates over twitter_list"""
        yield from self.data
        
    def __getitem__(self, idx):
        """enables indexing of twitter list"""
        return self.data[idx]
    
    def append(self,item):
        """ append one object to twitter list """
        self.data.append(item)
        
    def pop(self):
        """ get last object of twitter list and remove item from list """
        item = self.data[-1]
        self.data = self.data[:-1]
        return item
    
    def extend(self,item):
        """ extend twitter list by multiple objects """
        self.data.extend(item)
        
class FieldError(Exception):
    """Field error class. Given when required fields are not provided."""
    pass
        