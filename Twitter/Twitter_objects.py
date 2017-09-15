# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 23:13:47 2017

@author: Louis
"""
import abc
import Twitter

class Twitter_object:
    """ Twitter object """
    def __init__(self, **kwargs):
        """ Initiates class. Keyword arguments (twitter fields) stored as class 
        attriubutes. Empty cells stored as empty strings. List of twitter 
        fields which have been retrieved stored as self.fields 
        """
        self.api = Twitter.API.Api_control()
        self.fields = []
       
        for key,value in kwargs.items():
            if value:
                setattr(self,key,value)
            else:
                setattr(self,key,'')                
            self.fields.append(key)
        
    def print_object(self, *args):
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
    def __init__(self, **kwargs):
        """Initiates class. If any of the fields 'user','text' or 'tweet' 
        are not provided as **kwargs then an error is returned.
        """
        if not set(['user','text','tweet_id']) <= set(kwargs.keys()):
            raise KeyError('Either text, user or tweet_id field not ' +
                                  'provided.')
        super().__init__(**kwargs)
    
    def __str__(self):
        return '{}: {}'.format(self.user, self.text)
 
    
class User(Twitter_object):
    """User_subclass"""
    def __init__(self, **kwargs):
        """Initiates class. If either of the fields 'screen_name' or 'user_id' 
        are not provided as **kwargs then an error is returned.
        """
        
        if (not set(['user_id','screen_name','description']) 
                    <= set(kwargs.keys())):
            raise KeyError('Either user_id or screen_name field not ' +
                                  'provided.')
        super().__init__(**kwargs)
        self.proc = 0
        self.ncursor_followers = -1
        self.ncursor_followings = -1
        self.following_proc = 0
        self.followers_proc = 0
        self.fields.append('proc')
        self.fields.append('ncursor_followers')
        self.fields.append('ncursor_followings')
        self.fields.append('following_proc')
        self.fields.append('followers_proc')
    
    def __str__(self):
        return '{}: {}'.format(self.screen_name, self.description)
    
class Twitter_list(object):
    """Twitter list class. Defines a list of twitter objects."""
    def __init__(self):
        """Initialises class."""
        self._database_connector = None       
        self._control = None
        self.data = []
        
    def __len__(self):
        """Returns length of twitter list."""
        return len(self.data)
    
    def __iter__(self):
        """Iterates over twitter_list."""
        yield from self.data
        
    def __getitem__(self, idx):
        """Enables indexing of twitter list."""
        return self.data[idx]
        
    def pop(self):
        """Get last object of twitter list and remove item from list."""
        item = self.data[-1]
        self.data = self.data[:-1]
        return item
    
    def append(self, item):
        """Appends twitter object to list."""
        self.data.append(item)
    
    def extend(self, item):
        """Extend twitter list by multiple objects."""
        self.data.extend(item)    
    
    def set_mediator(self, mediator):
        self._control = mediator
         
    @abc.abstractmethod
    def cappend(self,item):
        """Creates twitter object and appends to list."""
        pass
    
    @abc.abstractmethod
    def insert(self,item):
        """Insert twitter list into database."""
        pass
    
    @abc.abstractmethod
    def retrieve(self,item):
        """Retrieve twitter list from database."""
        pass
        
        
class Tweet_list(Twitter_list):
    """Subclass of twitter list used for lists of tweets."""
    def cappend(self,item):
        """Reformats certain fields then appends tweet object to tweet list."""
        hashlst = []
        umlst = []
        url = []
        # 'Hashtag' field reformatted to single string.
        if not item['entities']['hashtags']:  
            [hashlst.append(it['text']) for it in item['entities']['hashtags']]
            hashlst = ','.join(hashlst)   
        # 'User_mentions' field reformatted to single string.
        if not item['entities']['user_mentions']:
            [umlst.append(it['text']) for it in item['entities']['user_mentions']]
            umlst = ','.join(umlst)
        # 'url' field extracted if 'entities' key exists in tweet output.
        if item['entities']['urls']:
            url = item['entities']['urls'][0]['display_url']
        
        self.data.append(Tweet(tweet_id = item['id'], 
                          date = item['created_at'], 
                          url = url, 
                          hashtags = hashlst, 
                          user_mentions = umlst,
                          user = item['user']['screen_name'],
                          text = item['text']))
        
    def insert(self,tablename='tweets'):
        """Checks required fields present in all tweet objects then inserts
        into 'tweets' table if so.
        """
        for tweet in self.data:
            if not set(['user','text','tweet_id','url','hashtags','date',
                        'user_mentions']) <= set(tweet.fields):
                raise KeyError('All required fields were not provided.')  
        #import pdb; pdb.set_trace()
        self._control._database_connector.insert_object(self,tablename)
    
    def retrieve(self,tablename='tweets',fields=None,**kwargs):
        """Retrieves data from database using specified fields and keyword
        arguments. See help Database_connector.retrieve for more information.
        """
        self._control._database_connector.retrieve(self,tablename,fields,
                                                  **kwargs)
        
    def process(self,keywords):
        """Returns the percentage of tweets containing a set of keywords.
        """
        self.keyword_scores = {}
        for keyword in keywords:
            score = 0
            for item in self.data:   
                if keyword in item.text.lower():
                    score += 1
                score = score/len(self.data)
            self.keyword_scores[keyword] = score
    
    
class User_list(Twitter_list):
    """Subclass of twitter list used for lists of users."""
    def cappend(self, **kwargs):
        """Reformats certain fields then appends user object to tweet list."""
        self.data.append(User(**kwargs))
        
    def insert(self,tablename='users'):
        """Checks required fields present in all user objects then inserts
        into 'users' table if so.
        """
        for user in self.data:
            if (not set(['user_id','screen_name','description']) 
                        <= set(user.fields)):
                raise KeyError('All required fields were not provided.')
        #import pdb; pdb.set_trace()
        self._control._database_connector.insert_object(self,tablename)
    
    def retrieve(self,tablename='users',fields=None,**kwargs):
        """Retrieves data from database using specified fields and keyword
        arguments. See help Database_connector.retrieve for more information.
        """        
        self._control._database_connector.retrieve(self,tablename,fields,**kwargs)
 