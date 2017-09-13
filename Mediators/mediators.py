# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 00:30:24 2017

@author: Louis
"""
import sqlite3
import Twitter
from Twitter.Twitter_objects import Twitter_object

        
class Mediator:
    def __init__(self):
        self.tweets = Twitter.Twitter_lists.Tweet_list(self)
        self.users = Twitter.Twitter_lists.User_list(self)
        self.network = Network(self)
    
    
    
 
       
class Database_connector:
    def insert(list_obj,tablename):
        """ inserts list of twitter objects into specified table."""
        # Connects to database.
        list_obj.db = sqlite3.connect(
                r'C:\Users\Louis\python\twitter_databases\twitdb.db')
        # Loop through tweets.
        for idx,obj in enumerate(list_obj.data):
            # Open database cursor.
            cursor = list_obj.db.cursor()
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
                list_obj.db.commit()
                print('Row inserted.')
            except sqlite3.Error:
                print('Unable to insert {}.'.format(str(idx)))
        # Close database.
        list_obj.db.close()
        
    def retrieve(list_obj,tablename,fields=None,**kwargs):
        """Retrieves data from database using specified fields and keyword
        arguments. Inputs:
            tablename: Name of table to retrieve data from.
            fields: Table fields to retrieve (the 'X' in SELECT X FROM....)
            **kwargs: Conditional arguments (anything after WHERE...).
            
            kwargs are formated so that the field is the kwarg name, and the
            conditional argument is the kwarg value (e.g. ...
                user_id = 'NOT IN(SELECT user_id FROM scores)' 
                user_name = '= louisbyrne'
                )
        """
        list_obj.db = sqlite3.connect(
                r'C:\Users\Louis\python\twitter_databases\twitdb.db')
        cursor = list_obj.db.cursor()
        # Creates string used to refine database search (everything after
        # WHERE...).
        criteria = []
        for key, value in kwargs.items():
            criteria.append(key + ' ' +  value)
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
            obj = Twitter_object(**kwargs)    
            list_obj.data.append(obj)
        list_obj.db.close()