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
'2g1c',
'2 girls 1 cup',
'acrotomophilia',
'anal',
'anilingus',
'anus',
'arsehole',
'ass',
'asshole',
'assmunch',
'auto erotic',
'autoerotic',
'babeland',
'baby batter',
'ball gag',
'ball gravy',
'ball kicking',
'ball licking',
'ball sack',
'ball sucking',
'bangbros',
'bareback',
'barely legal',
'barenaked',
'bastardo',
'bastinado',
'bbw',
'bdsm',
'beaver cleaver',
'beaver lips',
'bestiality',
'bi curious',
'big black',
'big breasts',
'big knockers',
'big tits',
'bimbos',
'birdlock',
'bitch',
'black cock',
'blonde action',
'blonde on blonde action',
'blow j',
'blow your l',
'blue waffle',
'blumpkin',
'bollocks',
'bondage',
'boner',
'boob',
'boobs',
'booty call',
'brown showers',
'brunette action',
'bukkake',
'bulldyke',
'bullet vibe',
'bung hole',
'bunghole',
'busty',
'butt',
'buttcheeks',
'butthole',
'camel toe',
'camgirl',
'camslut',
'camwhore',
'carpet muncher',
'carpetmuncher',
'chocolate rosebuds',
'circlejerk',
'cleveland steamer',
'clit',
'clitoris',
'clover clamps',
'clusterfuck',
'cock',
'cocks',
'coprolagnia',
'coprophilia',
'cornhole',
'cum',
'cumming',
'cunnilingus',
'cunt',
'darkie',
'date rape',
'daterape',
'deep throat',
'deepthroat',
'dick',
'dildo',
'dirty pillows',
'dirty sanchez',
'dog style',
'doggie style',
'doggiestyle',
'doggy style',
'doggystyle',
'dolcett',
'domination',
'dominatrix',
'dommes',
'donkey punch',
'double dong',
'double penetration',
'dp action',
'eat my ass',
'ecchi',
'ejaculation',
'erotic',
'erotism',
'escort',
'ethical slut',
'eunuch',
'faggot',
'fecal',
'felch',
'fellatio',
'feltch',
'female squirting',
'femdom',
'figging',
'fingering',
'fisting',
'foot fetish',
'footjob',
'frotting',
'fuck',
'fucking',
'fuck buttons',
'fudge packer',
'fudgepacker',
'futanari',
'g-spot',
'gang bang',
'gay sex',
'genitals',
'giant cock',
'girl on',
'girl on top',
'girls gone wild',
'goatcx',
'goatse',
'gokkun',
'golden shower',
'goo girl',
'goodpoop',
'goregasm',
'grope',
'group sex',
'guro',
'hand job',
'handjob',
'hard core',
'hardcore',
'hentai',
'homoerotic',
'honkey',
'hooker',
'hot chick',
'how to kill',
'how to murder',
'huge fat',
'humping',
'incest',
'intercourse',
'jack off',
'jail bait',
'jailbait',
'jerk off',
'jigaboo',
'jiggaboo',
'jiggerboo',
'jizz',
'juggs',
'kike',
'kinbaku',
'kinkster',
'kinky',
'knobbing',
'leather restraint',
'leather straight jacket',
'lemon party',
'lolita',
'lovemaking',
'make me come',
'male squirting',
'masturbate',
'menage a trois',
'milf',
'missionary position',
'motherfucker',
'mound of venus',
'mr hands',
'muff diver',
'muffdiving',
'nambla',
'nawashi',
'negro',
'neonazi',
'nig nog',
'nigga',
'nigger',
'nimphomania',
'nipple',
'nipples',
'nsfw images',
'nude',
'nudity',
'nympho',
'nymphomania',
'octopussy',
'omorashi',
'one cup two girls',
'one guy one jar',
'orgasm',
'orgy',
'paedophile',
'panties',
'panty',
'pedobear',
'pedophile',
'pegging',
'penis',
'phone sex',
'piece of shit',
'piss pig',
'pissing',
'pisspig',
'playboy',
'pleasure chest',
'pole smoker',
'ponyplay',
'poof',
'poop chute',
'poopchute',
'porn',
'porno',
'pornography',
'prince albert piercing',
'pthc',
'pubes',
'pussy',
'queaf',
'raghead',
'raging boner',
'rape',
'raping',
'rapist',
'rectum',
'reverse cowgirl',
'rimjob',
'rimming',
'rosy palm',
'rosy palm and her 5 sisters',
'rusty trombone',
's&m',
'sadism',
'scat',
'schlong',
'scissoring',
'semen',
'sex',
'sexo',
'sexy',
'shaved beaver',
'shaved pussy',
'shemale',
'shibari',
'shit',
'shota',
'shrimping',
'slanteye',
'slut',
'smut',
'snatch',
'snowballing',
'sodomize',
'sodomy',
'spic',
'spooge',
'spread legs',
'strap on',
'strapon',
'strappado',
'strip club',
'style doggy',
'suck',
'sucks',
'suicide girls',
'sultry women',
'swastika',
'swinger',
'tainted love',
'taste my',
'tea bagging',
'threesome',
'throating',
'tied up',
'tight white',
'tit',
'tits',
'titties',
'titty',
'tongue in a',
'topless',
'tosser',
'towelhead',
'tranny',
'tribadism',
'tub girl',
'tubgirl',
'tushy',
'twat',
'twink',
'twinkie',
'two girls one cup',
'undressing',
'upskirt',
'urethra play',
'urophilia',
'vagina',
'venus mound',
'vibrator',
'violet blue',
'violet wand',
'vorarephilia',
'voyeur',
'vulva',
'wank',
'wet dream',
'wetback',
'white power',
'women rapping',
'wrapping men',
'wrinkled starfish',
'xx',
'xxx',
'yaoi',
'yellow showers',
'yiffy',
'zoophilia']

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

    