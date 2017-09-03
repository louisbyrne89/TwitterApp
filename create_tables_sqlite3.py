# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 14:29:33 2017

@author: Louis
"""

import sqlite3
def create_table_tweets():
    db = sqlite3.connect('data/twitter')
    cursor = db.cursor()
    cursor.execute('''
                   CREATE TABLE tweets(
                                       id INTEGER PRIMARY KEY, 
                                       tweet_id INTEGER,
                                       search TEXT,
                                       date TEXT,
                                       url TEXT,
                                       hashtags TEXT,
                                       user_mentions TEXT,
                                       user TEXT,
                                       text TEXT
                                       )
                   ''')
    
    db.commit()
    db.close()
    
def create_table_users():
    db = sqlite3.connect('data/twitter')
    cursor = db.cursor()
    cursor.execute('''
                   CREATE TABLE users(
                                       user_id INTEGER PRIMARY KEY,
                                       screen_name TEXT,
                                       description TEXT,
                                       search TEXT,
                                       followers TEXT,
                                       following TEXT,
                                       DONE BOOLEAN
                                       
                                       )
                   ''')
    db.commit()
    db.close()
    
def drop_table(tablename):
    db = sqlite3.connect('data/twitter')
    cursor = db.cursor()
    cursor.execute('drop table ' + tablename)
    db.commit()
    db.close()
    