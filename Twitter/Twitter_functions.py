# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 20:32:14 2017

@author: Louis
"""
from Twitter.Twitter_objects import Tweet_list, User_list
import json


def get_user_tweets(control,user,count=2000):
    """Retrieves last 'count' tweets from user. Default set to 2000.
    Inputs:
        mediator: mediator instance
        user: user instance.
    """
    search = 'statuses/user_timeline'
    req = control._api_control.api.request(search, {'user_id': user.user_id,
                                                    'count': count,
                                                    'exculde_replies':'true',
                                                    'include rts': 'false'})
    return control.create_tweet_list(req)


def sample_tweets(control, search, indict):   
    """Samples latest tweets for keyword list.
    Inputs:
        mediator: mediator instance
        search: twitter feature to search
        indict: keywords to search
    """
    
    req = control._api_control.api.request(search,indict)
    return control.create_tweet_list(req,p2s=True), control.create_user_list(req)


def process_tweets(control, keywords):
    """Process tweets list to find percentage of tweets containing keywords.
    Keywords must be provided entirely as lower case as tweet is lowered.
    """
    #keywords = ['python','sql','junior','flexi',
    #            'remote','london','uk','bristol']
    user_list = User_list()
    user_list.set_mediator(control)
    user_id = '''NOT IN (SELECT user_id FROM scores)'''
    user_list.retrieve(user_id=user_id)
    for user in user_list:
        tweet_list = get_user_tweets(control,user)
        tweet_list.process(keywords)
        keyword_scores = tweet_list.keyword_scores
    


def get_following(control, user, cursor=-1):
    """Return users followers as user list. Also updates table with
    latest cursor."""
    search = 'friends/list'
    req = control._api_control.api.request(search,{'user_id':user.user_id,
                                                   'count':200,
                                                   'cursor':cursor})
    txt = json.loads(req.text)
    
    if txt['users']:
        fields = {'ncursor_following':txt['next_cursor']}
        control._database_connector.update('users',fields,user_id=
                                           '=' + str(user.user_id))
        
        return control.create_user_list(txt['users'], obj = 'user') 
    else:
        fields = {'ncursor_following':'0','following_proc':'1'} 
        control._database_connector.update('users',fields,user_id=
                                           '=' + str(user.user_id))
        return []
        
              
def get_followers(control,user,cursor=-1):
    """Return users followings as user list. Also updates table with
    latest cursor."""
    search = 'followers/list'
    req = control._api_control.api.request(search,{'user_id':user.user_id,
                                                   'count':200,
                                                   'cursor':cursor})
    txt = json.loads(req.text)
    if txt['users']:
        fields = {'ncursor_followers':txt['next_cursor']}
        control._database_connector.update('users',fields,user_id=
                                           '=' + str(user.user_id))
        
        return control.create_user_list(txt['users'], obj = 'user') 
    else:
        fields = {'ncursor_followers':'0','followers_proc':'1'} 
        control._database_connector.update('users',fields,user_id=
                                           '=' + str(user.user_id))                                           
        return []
    
