# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 00:30:24 2017

@author: Louis
"""
import sqlite3
import Twitter
from Twitter.Twitter_objects import Twitter_object, Tweet, User
import datetime
import time
from TwitterAPI import TwitterAPI as tw
import json

class Api_control:
    """This class controls interactions with the TwitterAPI."""  
    def __init__(self):
        """Twitter API keys loaded from file and API connects to API."""
        self._control = None
        with open(r'C:\Users\Louis\python\twitter_not_git\keys.txt', 'r') as f:
            keys = json.load(f)
            
        self.api = tw(keys['consumer_key'],
                   keys['consumer_secret'],
                   keys['access_token'],
                   keys['access_token_secret'])
        self.quotas = {}
        
    def set_mediator(self,mediator):
        self._control = mediator
        
    def request(self,search,indict):
        """Makes API request. If quota is used up then process is delayed for
        15 minutes. Input arguments:
            search: Twitter API resource to query.
            indict: filter parameters
        """
        while 1:
            if search not in self.quotas.keys() or self.quotas[search]:
                req = self.api.request(search, indict)              
                quota = req.get_rest_quota()['remaining']
                #import pdb; pdb.set_trace()
                self.update_usage_limits(search,quota)
                return req
            else:
                print('Quota used for "{}". Sleeping for 15 minutes.'.format(
                        search))
                time.sleep(900)
    
    def update_usage_limits(self,search,quota):
        """Update Api_control with new Twitter rate quota following request.
        Input arguments:
            search: Twitter API resource to query.
            indict: filter parameters
        """
        ti = datetime.datetime.now()
        self.quotas[search] = {'quota':quota,'time':ti}
        #import pdb; pdb.set_trace()
         
       
class Database_connector:
    def insert_object(list_obj,tablename):
        """Inserts list of twitter objects into specified table. 
        Input arguments:
            list_obj: twitter or user list.
            tablename: name of table to insert data into.
        """
        # Connects to database.
        db = sqlite3.connect(
                r'C:\Users\Louis\python\twitter_databases\twitdb.db')
        # Loop through tweets.
        for idx,obj in enumerate(list_obj.data):
            # Open database cursor.
            cursor = db.cursor()
            # Create query insert statement string using comma delimited
            # fields ('fields'), question marks ('questions') and a list of
            # the values to be inserted (varil)    
            fields = ','.join(obj.fields)
            questions = ','.join('?' * len(obj.fields)) 
            varil = [getattr(obj,fi) for fi in obj.fields]
            instr = ('INSERT INTO {}({}) VALUES ({})'
                     .format(tablename,fields,questions))
            # Attempts to insert data.
            try:
                cursor.execute(instr,varil)
                db.commit()
                print('Row inserted.')
            except sqlite3.Error:
                print('Unable to insert {}.'.format(str(idx)))
        # Close database.
        db.close()
    
    def insert(tablename, fields, **kwargs):
        db = sqlite3.connect(
                r'C:\Users\Louis\python\twitter_databases\twitdb.db')
        cursor = db.cursor()
        fieldstr = ', '.join(list(fields.keys()))
        questions = ','.join('?' * len(fields))
        instr = 'INSERT INTO {}({}) VALUES ({})'.format(tablename,fieldstr,
                                                        questions)
        varil = list(fields.values())
        cursor.execute(instr,varil)
        db.commit()
        db.close()
        print('Row inserted.')

        
        
    def update(tablename,fields,**kwargs):
        """Updates table. Input arguments:
                tablename: name of table to update.
                fields: fields to update. Dictionary with key = field and
                value = value.
                **kwargs: conditional arguments (e.g. user_id to update).
                key = field and value = contitional argument (e.g. '= 100')
                
        Multiple fields and kwargs can be provided.
        """
        db = sqlite3.connect(
                r'C:\Users\Louis\python\twitter_databases\twitdb.db')
        cursor = db.cursor()
        fieldstr = ', '.join(['{} = {}'.format(key,value) 
                             for key,value in fields.items()])
    
        critstr = ' AND '.join(['{} {}'.format(key,value) for key,value
                                in kwargs.items()])
                
        upstr = 'UPDATE {} SET {} WHERE {}'.format(tablename, fieldstr, 
                                                   critstr)
        #import pdb; pdb.set_trace()
        cursor = cursor.execute(upstr)     
                
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
        db = sqlite3.connect(
                r'C:\Users\Louis\python\twitter_databases\twitdb.db')
        cursor = db.cursor()
        # Creates string used to refine database search (everything after
        # WHERE...).
        critstr = ' AND '.join(['{} {}'.format(key,value) for key,value
                                in kwargs.items()])
        # Returns fields which will be retrieved from the database. If fields
        # are provided to function, these are reformatted to string. If no
        # fields are provided, 'fields' populated by requesting all the table 
        # fields from the datbase.
        if fields:
            fistr = ','.join(fields)
            selstr = 'SELECT {} FROM {}'.format(fistr,tablename)
        else:
            selstr = 'SELECT * FROM ' + tablename
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
        db.close()
        