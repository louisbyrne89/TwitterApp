# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 23:13:47 2017

@author: Louis
"""
import sqlite3

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
        """Prints tweet to string. Option arguments specifying attributes to
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
            string = string + key + ': ' + val + '\n'
        return print(string)
            
    class FieldError(Exception):
        """Field error class. Given when required fields are not provided."""
        pass
        
        
class Tweet(Twitter_object):
    """Tweet subclass"""
    def __init__(self,**kwargs):
        """Initiates class. If any of the fields 'user','text' or 'tweet' 
        are not provided then an error is returned."""
        super().__init__(**kwargs)
        if not set(['user','text','tweet_id']) < set(kwargs.keys()):
            raise self.FieldError('Either text, user or tweet_id field not ' +
                                  'provided.')
    
    def __str__(self):
        return self.user + ': ' + self.text
    
    def insert(self):
        """ Inserts tweet into sqlite3 database."""
        # Connects to database and creates database cursor object.
        db = sqlite3.connect('data/twitter')
        cursor = db.cursor()
        cursor = cursor.execute('select tweet_id from tweets')
        ids = cursor.fetchall()
        if (self.tweet_id,) not in ids:
            # Converts tweet field attribute into string, and creates a string 
            # of question marks which are required for input statement.
            fields = ','.join(self.fields)
            questionl = ['?'] * len(fields.split(','))
            questions = ','.join(questionl)
            varil = [getattr(self,fi) for fi in self.fields]
            
            instr = ('INSERT INTO tweets(' + fields + 
                    ') VALUES (' + questions+')')
            cursor.execute(instr,varil)
            db.commit()
            db.close()
            print('tweet inserted')
        
class User(Twitter_object):
    """User_subclass"""
    def __init__(self,**kwargs):
        """Initiates class. If either of the fields 'screen_name' or 'user_id' 
        are not provided then an error is returned."""
        super().__init__(**kwargs)
        if (not set(['user_id','screen_name','description']) 
                    < set(kwargs.keys())):
            raise self.FieldError('Either user_id or screen_name field not ' +
                                  'provided.')
    
    def __str__(self):
        return self.user + ': ' + self.text
    
    def insert(self):
        """ Inserts user into sqlite3 database."""
        # Adds boolean parameter for processed user switch.
        self.done = 0
        self.fields.append('done')
        # Connects to database and creates database cursor object.
        db = sqlite3.connect('data/twitter')
        cursor = db.cursor()
        ids = cursor.execute('select user_id from users')
        if (self.user_id,) not in ids:
            # Converts tweet field attribute into string, and creates a string of
            # question marks which are required for input statement.
            fields = ','.join(self.fields)
            questionl = ['?'] * len(fields.split(','))
            questions = ','.join(questionl)
            varil = [getattr(self,fi) for fi in self.fields]
            
            instr = ('INSERT INTO users(' + fields + 
                    ') VALUES (' + questions+')')
            cursor.execute(instr,varil)
            db.commit()
            db.close()
            print('user inserted')
   

        
