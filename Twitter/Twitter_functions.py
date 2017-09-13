# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 03:13:22 2017

@author: Louis
"""
from Twitter.Twitter_objects import Tweet, User
from Twitter.Twitter_lists import Tweet_list, User_list
from Mediators.mediators import Api_control
from Mediators.mediators import Mediator

def create_tweet_object(item):
    """Creates a single tweet object. Requres one input:
            item, which is an object comprising a singe tweet fetched from api.
    """        
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
    # Important fieds from tweet extracted and saved as new object
    Tweet_ins = Tweet(tweet_id = item['id'],
                   date = item['created_at'],
                   url = url,
                   hashtags = hashlst,
                   user_mentions = umlst,
                   user = item['user']['screen_name'],
                   text = item['text'])
    return Tweet_ins


def create_user_object(item):
    """Creates a single user object. Requires one input:
            item, which is an object comprising a singe tweet fetched from api.
    """
    # Important fieds from tweet extracted and saved as new object
    User_ins = User(screen_name = item['user']['screen_name'],
                 description = item['user']['description'],
                 user_id = item['user']['id'])
    return User_ins

    
def sampling(api,search,indict):
    """Samples twitter using either search or stream methods. Three inputs:
        api: api connection object
        search: twitter search method
        indict: dictionary of search parameters
    """
    # make API request.
    api = Api_control()
    api.request(search,indict)
    req = api.req
    #req = api.request(search, indict)
    for item in req:
            print(item['text'] if 'text' in item else item)
            if len(item)>1:
                # Create tweet and user instances
                Tweet_ins = create_tweet_object(item)
                User_ins = create_user_object(item)
                # Create or append single tweet/user instances to list
                if 'tweet_list' not in locals():
                    tweet_list = Tweet_list(obj=Tweet_ins)
                else:
                    tweet_list.append(Tweet_ins)
                    
                if 'user_list' not in locals():
                    user_list = User_list(obj=User_ins)
                else:
                    user_list.append(User_ins)            
    return tweet_list, user_list    