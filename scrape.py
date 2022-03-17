import tweepy
from decouple import config
import json
import csv
import helper

bearer_token = config('bearerToken',default='')
consumer_key = config('consumer_key',default='')
consumer_secret = config('consumer_secret',default='')
access_token = config('accessToekn',default='')
access_token_secret = config('accessTokenSecret',default='')

def getAPIV1():
  authenticator = tweepy.OAuthHandler(consumer_key, consumer_secret)
  authenticator.set_access_token(access_token, access_token_secret)
  api = tweepy.API(authenticator, wait_on_rate_limit=True)
  return api

def getClientV2():
  client = tweepy.Client(bearer_token=bearer_token, 
                        consumer_key=consumer_key, 
                        consumer_secret=consumer_secret, 
                        access_token=access_token, 
                        access_token_secret=access_token_secret)
  
  return client

def getUserInfo(username):
  client = getClientV2()
  user = client.get_user(username=username)
  return user.data.id

def getTweets(tag):
  api = getAPIV1()
  tweet_cursor = tweepy.Cursor(api.search_tweets, q=tag, lang="en", tweet_mode="extended").items(100)
  # tweets = [tweet.full_text for tweet in tweet_cursor]
  tweets = [tweet._json for tweet in tweet_cursor]
  return tweets

def getFollowers():
  client = getClientV2()
  userID = getUserInfo('chen_haifan')
  followers = client.get_users_followers(id=userID)
  return followers.data

def getMe():
  api = getAPIV1()
  me = api.get_followers()
  return me

# tweets = getTweets('nft')
# json_object = json.loads(tweets[0]._json)
# json_formatted_str = json.dumps(json_object, indent=2)
# print(json_formatted_str)
# print(tweets[0])
# for i in range(len(tweets)):
#   print(i, " ", tweets[i]['user']['id'], '\n')

def getRecentTweeter(topic, filename):
  people = getTweets(topic)
  for i in range(len(people)):
    person = people[i]['user']
    data = [person['id'], person['name'],
            person['screen_name'], person['location'], person['description'], person['followers_count'], person['friends_count'], person['listed_count'], person['created_at'], person['favourites_count'], person['time_zone'], person['verified'], person['statuses_count'], person['lang'], person['following'], person['follow_request_sent']]
    # check if this person is already in the database
    idList = helper.readCol(filename, 'id')
    if str(person['id']) not in idList:
      helper.writeToFile(filename, data)


getRecentTweeter('nft', './data/people.csv')
