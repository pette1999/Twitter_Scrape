import tweepy
from decouple import config
import json
import csv
import helper
import time
from datetime import date
import datetime
import logging

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
  #client = getClientV2()
  api = getAPIV1()
  #user = client.get_user(username=username)
  user2 = api.get_user(screen_name=username)
  return user2._json

def getTweets(tag,mode):
  api = getAPIV1()
  tweet_cursor = tweepy.Cursor(api.search_tweets, q=tag, lang="en", result_type=mode, tweet_mode="extended").items(100)
  # tweets = [tweet.full_text for tweet in tweet_cursor]
  tweets = [tweet._json for tweet in tweet_cursor]
  return tweets

def reply(reply, tweetID):
  api = getAPIV1()
  api.update_status(status=reply, in_reply_to_status_id=tweetID,  auto_populate_reply_metadata=True)

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

def writeToBlacklist(filename, username):
  api = getAPIV1()
  users = tweepy.Cursor(
      api.get_friend_ids, screen_name=username, count=5000).items()
  requests = tweepy.Cursor(
      api.outgoing_friendships).items(5000)
  ids = helper.readCol(filename, 'id')
  users2 = list(users).copy()
  requests2 = list(requests).copy()
  if len(ids) >  0:
    for i in ids:
      if len(i) > 0 and int(i) not in list(users2) and int(i) not in list(requests2):
        print(type(int(i)), int(i) not in list(users2), int(i) not in list(requests2))
        # write the id to blacklist
        helper.writeToFile('./data/blacklist.csv', [i])
        # remove the id from following
        helper.deleteLine('./data/following.csv', i)

def getFollowingIDs(filename, username):
  api = getAPIV1()
  users = tweepy.Cursor(
      api.get_friend_ids, screen_name=username, count=5000).items()
  requests = tweepy.Cursor(
      api.outgoing_friendships).items(5000)
  # read in what we have in file
  ids = helper.readCol(filename, 'id')
  status = helper.readCol(filename, 'status')
  blacklist = helper.readCol('./data/blacklist.csv', 'id')
  # if id is in ids but not in users, it means we unfollowed him, move to blacklist
  writeToBlacklist(filename, username)
  while True:
    try:
      user = next(users)
    except tweepy.errors.TweepyException:
      time.sleep(60*15)
      user = next(users)
    except StopIteration:
      break
    # check if we already have the person in our list
    if str(user) not in ids:
      helper.writeToFile(filename, [str(user),True])
    if str(user) in ids and status[ids.index(str(user))] == 'False':
      # the user approved out following request
      helper.editFile('./data/following.csv', str(user), [str(user), True])
  while True:
    try:
      request = next(requests)
    except tweepy.errors.TweepyException:
      time.sleep(60*15)
      request = next(requests)
    except StopIteration:
      break
    # check if we already have the person in our list
    if str(request) not in ids:
      helper.writeToFile(filename, [str(request), False])

def getFollowerIDs(followerFilename, username):
  api = getAPIV1()
  followers = tweepy.Cursor(
      api.get_follower_ids, screen_name=username, count=5000).items()
  followerIDs = helper.readCol(followerFilename, 'id')
  while True:
    try:
      follower = next(followers)
    except tweepy.errors.TweepyException:
      time.sleep(60*15)
      follower = next(followers)
    except StopIteration:
      break
    # check if we already have the person in our list
    if str(follower) not in followerIDs:
      helper.writeToFile(followerFilename, [str(follower)])

def getOutgoing_friendship(filename):
  api = getAPIV1()
  users = tweepy.Cursor(
      api.outgoing_friendships).items(5000)
  # read in what we have in file
  ids = helper.readCol(filename, 'id')
  while True:
    try:
      user = next(users)
    except tweepy.errors.TweepyException:
      time.sleep(60*15)
      user = next(users)
    except StopIteration:
      break
    # check if we already have the person in our list
    if str(user) not in ids:
      helper.writeToFile(filename, [str(user), False])

def getRecentTweeter(topic, filename):
  people = getTweets(topic, 'recent')
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

def unFollowUser(userID):
  client = getClientV2()
  client.unfollow_user(target_user_id=userID)

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
    print("Doesn't have permission to send direct messages to: ", userID)

def followAndHello(filename, myUsername):
  final_target_ids = []
  # run through the targeting people list and get all there ids
  idList = helper.readCol('./data/people.csv', 'id')
  # run through the current following list, # check if already sent a follow request, check if already followed these people, check if in the blacklist
  getFollowingIDs(filename, myUsername)
  following = helper.readCol('./data/following.csv', 'id')
  blacklist = helper.readCol('./data/blacklist.csv', 'id')
  sentFollow = helper.readCol('./data/sentFollow.csv', 'id')
  if len(idList) > 0:
    for i in idList:
      if i not in following and i not in blacklist:
        final_target_ids.append(i)
    for j in final_target_ids:
      # follow these people
      if j not in sentFollow:
        print(final_target_ids.index(j))
        try:
          followUser(j)
          d = helper.convertDate_to_days(date.today().strftime("%m/%d/%y"))
          helper.writeToFile('./data/sentFollow.csv', [j, d])
          # send direct message to these people
          sendDirectMessage(j, "Hello")
        except:
          continue
  # the limit is 50 people/15 min
  # clear the people.csv file
  helper.clearFile('./data/people.csv', ['id', 'name', 'username', 'location', 'description', 'followers_count', 'friends_count', 'listed_count', 'date_joined', 'favourites_count', 'time_zone', 'verified', 'statuses_count', 'language', 'current_following', 'follow_request_sent'])
  time.sleep(2)
  getFollowingIDs(filename, myUsername)

def check():
  toUnfollow = []
  # pull the account followers to file
  getFollowerIDs('./data/follower.csv', 'PeterCh39124642')
  followerIDs = helper.readCol('./data/follower.csv', 'id')
  # filter out all the people in the `sentFollow.csv` that have past the time LIMIT(7 days)
  filteredIDs = [] # users that needed to be checked if they followed or not
  d = helper.convertDate_to_days(date.today().strftime("%m/%d/%y"))
  sendFollowIDs = helper.readCol('./data/sentFollow.csv', 'id')
  sendFollowDates = helper.readCol('./data/sentFollow.csv', 'date')
  for i in range(len(sendFollowDates)):
    if int(sendFollowDates[i]) < int(d)-1:
      filteredIDs.append(sendFollowIDs[i])
  # check each id in the filteredIDs list and see if it's in the followerIDs list
  # if yes, then the user followed back, if not, the user didn't follow back and we need to unfollow this user as well
  for j in filteredIDs:
    if j in followerIDs:
      # the user followed back
      pass
    else:
      # the person didn't follow back
      # unfollow this person
      toUnfollow.append(j)
      helper.deleteLine('./data/following.csv', j)
      helper.writeToFile('./data/blacklist.csv', [j])

    helper.deleteLine('./data/sentFollow.csv', j)
   
  for people in toUnfollow:
    unFollowUser(people)
    print(people, " unfollowed.")

def replyRecentTweets(topic):
  message = "🌟 Please checkout our new generative art Spectrum by @LibertasART"
  replyList = []
  tweets = getTweets(topic, 'recent')
  logging.basicConfig(filename="./data/log.log",level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
  # print(tweets)
  for i in range(len(tweets)):
    if tweets[i]['user']['followers_count'] > 10000:
      replyList.append(i)
  for j in replyList:
    # reply to these tweets
    reply(message, tweets[j]['id_str'])
    logging.info('replied to this id:'+ str(tweets[j]['id_str']))
    print(tweets[j]['id_str'])
  print(replyList)


# followAndHello('./data/following.csv', 'chen_haifan')
# print(helper.convertDate_to_days('1/31/22'))
# check()
# replyRecentTweets('drop%20your%20nft')
