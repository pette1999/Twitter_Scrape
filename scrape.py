import tweepy
from decouple import config

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

def getTweets():
  api = getAPIV1()
  tweet_cursor = tweepy.Cursor(api.search_tweets, q= 'nft', lang="en", tweet_mode="extended").items(100)
  # tweets = [tweet.full_text for tweet in tweet_cursor]
  tweets = [tweet for tweet in tweet_cursor]
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

# tweets = getTweets()
# print(tweets)
followers = getFollowers()
print(followers)