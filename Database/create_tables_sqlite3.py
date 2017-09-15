# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 14:29:33 2017

@author: Louis
"""

import sqlite3
def create_table_tweets():
    db = sqlite3.connect(r'C:\Users\Louis\python\twitter_databases\twitdb.db')
    cursor = db.cursor()
    cursor.execute('''
                   CREATE TABLE tweets(tweet_id INTEGER PRIMARY KEY,
                                       date TEXT,
                                       url TEXT,
                                       hashtags TEXT,
                                       user_mentions TEXT,
                                       user TEXT NOT NULL,
                                       text TEXT NOT NULL
                                       )
                   ''')
    
    db.commit()
    db.close()
    
def create_table_users():
    db = sqlite3.connect(r'C:\Users\Louis\python\twitter_databases\twitdb.db')
    cursor = db.cursor()
    cursor.execute('''
                   CREATE TABLE users( user_id INTEGER PRIMARY KEY,
                                       screen_name TEXT NOT NULL,
                                       description TEXT NOT NULL,
                                       proc BOOLEAN NOT NULL,
                                       ncursor_followers INTEGER NOT NULL,
                                       ncursor_followings INTEGER NOT NULL,
                                       followings INTEGER NOT NULL,
                                       followers INTEGER NOT NULL,
                                       following_proc BOOLEAN NOT NULL,
                                       followers_proc BOOLEAN NOT NULL
                                       )
                   ''')
    db.commit()
    db.close()
 
    
def create_table_scores():
    db = sqlite3.connect(r'C:\Users\Louis\python\twitter_databases\twitdb.db')
    cursor = db.cursor()
    cursor.execute('''
                   CREATE TABLE scores(user_id INTEGER NOT NULL,
                                       keyword TEXT NOT NULL,
                                       tweets_score INTEGER NOT NULL,
                                       FOREIGN KEY(user_id) REFERENCES users(user_id)
                                       )
                   ''');
    db.commit()
    db.close()
 
    
def drop_table(tablename):
    db = sqlite3.connect(r'C:\Users\Louis\python\twitter_databases\twitdb.db')
    cursor = db.cursor()
    cursor.execute('drop table ' + tablename)
    db.commit()
    db.close()
    