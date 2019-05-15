#!/usr/bin/env python

"""

Code by Callum Mulligan

Uses several libraries inlcuding the Tweepy Library to collect 500 tweets, collates the tweets and then makes a haiku
tries to account for profanities and special characters. 

Warning, the bad words are in this file.

"""

#Makes a haiku from tweets

import tweepy
import csv
import random
import time
import json
import re
import urllib
import emoji

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

####input your credentials here
consumer_key = 'Consumer Key'
consumer_secret = 'Public Key'
access_token = 'Access Tocket'
access_token_secret = 'Acces Tocken Secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,timeout = 20, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

tweets = []

syl_five = []
syl_seven = []
poem = []

#Profanity Filter --> List found here: https://stackoverflow.com/questions/3531746/what-s-a-good-python-profanity-filter-library

arrBad = [
]

filename = "Filter.txt"
file = open(filename, "r")
for line in file:
    load = line.split(',')
    d = {}
    arrBad.append(load[0])

def getTweets(Search):
    data = api.rate_limit_status()

    print (data['resources']['search']['/search/tweets'])
    print("Getting Tweets")
    timeout = time.time() + 10 
    for tweet in tweepy.Cursor(api.search,q=Search,count=500,
                            lang="en",timeout="5").items(): #timeout isnt needed and most likely does nothing.
        

        tweets.append(tweet)
        
        
        if time.time() > timeout or len(tweets) > 500:
            break

    print("Number of Tweets:   "+ str(len(tweets)))


def syllable_count(word):
    
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count

def sortTweets():
    for tweet in tweets:
        tweet_text_array = tweet.text.split(" ")
        total_syl = 0
        sentance = ""
        for word in tweet_text_array:
            word = word.lower()
                     
            if word is "" or word is " " or len(word) is 0 or "http" in word or "@" in word or "rt" in word:
                continue
            if word in arrBad:
                break
            
            word = word.replace("'"," ")
            word = word.replace("’"," ")
            word = word.replace('"'," ")
            
            syl = syllable_count(word)
            total_syl = total_syl + syl
            sentance = sentance + " " + word
            
            if total_syl is 5:
                syl_five.append(emoji.demojize(sentance)) #We shouldnt neeed the deemojze

            if total_syl is 7:
                syl_seven.append(emoji.demojize((sentance)))
                sentance = ""
                total_syl  = 0
            if total_syl > 7:
                sentance = ""
                total_syl  = 0

def getPoem():
    global poem 
    poem = []
    poem.append(syl_five[random.randint(0,len(syl_five))-1])
    poem.append(syl_seven[random.randint(0,len(syl_seven)-1)])
    poem.append(syl_five[random.randint(0,len(syl_five)-1)])

    return poem


if __name__ == '__main__':

    getTweets('#Brexit')
    sortTweets()
    print(getPoem())

    