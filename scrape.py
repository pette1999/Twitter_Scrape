import tweepy
from decouple import config
import json
import csv
import helper
import time

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
                        access_token_secret=access_token_secret,
                        wait_on_rate_limit=True)
  
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

def getFollowers_by_username(username):
  api = getAPIV1()
  users = tweepy.Cursor(
      api.get_followers, screen_name=username, count=200).items()
  follower = []
  i = 0
  while True:
    try:
      user = next(users)
    except tweepy.errors.TweepyException:
      time.sleep(60*15)
      user = next(users)
    except StopIteration:
      break
    print(i, ' ', user._json)
    i += 1
    # follower.append(user._json)

def getFollowers_by_id(userID):
  api = getAPIV1()


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
    # check if the person is in our blacklist
    blackList = helper.readCol('./data/blacklist.csv', 'id')
    # check if we already followed this person or already sent a request
    if str(person['id']) not in idList and person['following'] == False and person['follow_request_sent'] == False and str(person['id']) not in blackList:
      helper.writeToFile(filename, data)

def followUser(userID):
  client = getClientV2()
  client.follow_user(target_user_id=userID)

def sendDirectMessage(userID, message):
  api = getAPIV1()
  options = [
      {
          "label": "I'm good",
          "description": "It means you're doing good",
          "metadata": "external_id_1"
      },
      {
          "label": "Not so good",
          "description": "It means you're not doing good",
          "metadata": "external_id_2"
      }
  ]
  try:
    api.send_direct_message(recipient_id=userID, text=message, quick_reply_options=options)
  except Exception as e:
    print(e)

def followAndHello(filename):
  # run through the list and get all there ids
  idList = helper.readCol(filename, 'id')
  # check if already followed these people

  # check if already sent a follow request
  # follow these people
  # send direct message to these people
  # follow every 30 seconds


# sendDirectMessage('1504937972453371908', "hello Peter!")
# followUser('1504696465918111744')
# print(getUserInfo('ChenHaifan3'))
# getRecentTweeter('nft','./data/people.csv')
print(getFollowers_by_username('rmaxb96'))
