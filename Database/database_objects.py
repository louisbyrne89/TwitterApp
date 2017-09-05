# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 16:03:16 2017

@author: Louis
"""
import sqlite3

import Twitter.Twitter_objects as to

class Twitter_list_db(to.Twitter_list):        
    def insert(self,tablename):
        """ inserts list of twitter objects into specified table."""
        # Connects to database.
        self.db = sqlite3.connect(
                r'C:\Users\Louis\python\twitter_databases\twitdb.db')
        # Loop through tweets.
        for idx,obj in enumerate(self.data):
            # Open database cursor.
            cursor = self.db.cursor()
            # Create query insert statement string using comma delimited
            # fields ('fields'), question marks ('questions') and a list of
            # the values to be inserted (varil)    
            fields = ','.join(obj.fields)
            questions = ','.join('?' * len(fields.split(','))) 
            varil = [getattr(obj,fi) for fi in obj.fields]
            instr = ('INSERT INTO {}({}) VALUES ({})'
                     .format(tablename,fields,questions))
            # Attempts to insert data.
            #import pdb; pdb.set_trace()
            try:
                cursor.execute(instr,varil)
                self.db.commit()
                print('Row inserted.')
            except sqlite3.Error:
                print('Unable to insert {}.'.format(str(idx)))
        # Close database.
        self.db.close()
        
    def retrieve(self,tablename,fields=None,**kwargs):
        """Retrieves data from the database and stores as tweet objects in
        'data'."""
        self.db = sqlite3.connect(
                r'C:\Users\Louis\python\twitter_databases\twitdb.db')
        cursor = self.db.cursor()
        # Creates string used to refine database search (everything after
        # WHERE...).
        criteria = []
        for key, value in kwargs.items():
            criteria.append(key + value)
        critstr = ' AND '.join(criteria)
        # Returns fields which will be retrieved from the database. If fields
        # are provided to function, these are reformatted to string. If no
        # fields are provided, 'fields' populated by requesting all the table 
        # fields from the datbase.
        if fields:
            fistr = ','.join(fields)
            selstr = 'SELECT {} FROM {}'.format(fistr,tablename)
        else:
            selstr = 'SELECT * from ' + tablename
            ficrs = cursor.execute('PRAGMA table_info({})'.format(tablename))
            fiftch = ficrs.fetchall()
            fields = [fiftch[i][1] for i,fie in enumerate(fiftch)]
        
        if kwargs:
            selstr = selstr + ' WHERE ' + critstr
        # Get data from database
        cursor = cursor.execute(selstr)
        data = cursor.fetchall()
        
        # Create twitter objects and append to 'data' attribute.        
        for row in data:
            kwargs = dict([(col, row[i]) for i,col in enumerate(fields)])
            obj = to.Twitter_object(**kwargs)    
            self.data.append(obj)
        self.db.close()

class Tweet_list_db(Twitter_list_db):
    def insert(self,tablename='tweets'):
        """ Adds a check that all required fields are present before inserting
        the data. """
        for tweet in self.data:
            if not set(['user','text','tweet_id','url','hashtags','date',
                        'user_mentions']) <= set(tweet.fields):
                raise to.FieldError('All required fields were not provided.')
            
        super().insert(tablename)
    
    def retrieve(self,tablename='tweets',fields=None,**kwargs):
        """Specifies 'tweets' table as default"""
        super().retrieve(tablename=tablename,fields=fields,**kwargs)
    
class User_list_db(Twitter_list_db):
    def insert(self,tablename='users'):
        """ Adds a check that all required fields are present before inserting
        the data. """
        for user in self.data:
            if (not set(['user_id','screen_name','description']) 
                        <= set(user.fields)):
                raise to.FieldError('Either user_id or screen_name field not ' +
                                  'provided.')
        super().insert(tablename=tablename)
    
    def retrieve(self,tablename='users',fields=None,**kwargs):
        """Specifies 'users' table as default"""
        super().retrieve(tablename=tablename,fields=fields,**kwargs)
#class Scoresdb(Parentdb):
    