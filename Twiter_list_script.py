# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 14:15:59 2017

@author: Louis
"""

from Twitter.Twitter_objects import Twitter_list

tl = Twitter_list()

tl.retrieve('users',fields=['user_id','screen_name'],user_id='>0')

