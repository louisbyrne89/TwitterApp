# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 13:33:57 2017

@author: Louis
"""
from Twitter_objects import Tweet, User, Twitter_object 
import sqlite3

class Twitter_list:
    """Twitter list class"""
    def __init__(self,columns=None,data=None,obj=None):
        """Initiates function. If data is provided when class is initiated,
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
    
    def retrieve(self,tablename,fields=None,**kwargs):
        """Retrieves data from the database and stores as tweet objects in
        'data'."""
        # Connects to database.
        db = sqlite3.connect('data/twitter')
        cursor = db.cursor()
        # Creates string used to refine database search (everything after
        # WHERE...).
        criteria = []
        for key, value in kwargs.items():
            criteria.append(key + value)
        critstr = ' AND '.join(criteria)
        # Returns fields which have been retrieved from the database. If fields
        # are provided to function, these are reformatted to string. If no
        # fields are provided, code assumes all fields are desired and
        # populates 'fields' by requesting the table fields from the datbase.
        if fields:
            fistr = ','.join(fields)
            selstr = ('SELECT ' + fistr +' FROM ' + tablename + 
                      ' WHERE ' + critstr)
        else:
            selstr = 'SELECT * from ' + tablename + ' WHERE ' + critstr
            ficrs = cursor.execute('PRAGMA table_info( '+ tablename + ')')
            fiftch = ficrs.fetchall()
            fields = [fiftch[i][1] for i,fie in enumerate(fiftch)]
 
        # Get data
        cursor = cursor.execute(selstr)
        data = cursor.fetchall()
        
        # Create twitter objects and append to 'data' attribute.        
        for row in data:
            kwargs = dict([(col, row[i]) for i,col in enumerate(fields)])
            obj = Twitter_object(**kwargs)                
            self.data.append(obj)
            
        db.close()
             
        return data
    
    def append(self,obj):
        self.data.append(obj)
