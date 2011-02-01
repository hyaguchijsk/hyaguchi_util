#!/usr/bin/env python

import os,tweepy

def read_auth_file(fname):
    f=open(fname)
    ret=f.readline().strip()
    f.close()
    return ret

def tweetstring(twstr):
    homedir=os.environ.get("HOME")
    consumer_key=read_auth_file(homedir + "/.twitter_consumer_key")
    consumer_secret=read_auth_file(homedir + "/.twitter_consumer_secret")
    access_key=read_auth_file(homedir + "/.twitter_access_key")
    access_secret=read_auth_file(homedir + "/.twitter_access_secret")

    auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_key,access_secret)
    twapi=tweepy.API(auth)
    twapi.update_status(twstr)
    
