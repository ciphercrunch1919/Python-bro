import tweepy

auth = tweepy.OAuthHandler('API_key', 'API_key_secret')
auth.set_access_token('Access_token_key', 'Access_token_key_secret')

api = tweepy.API(auth)

print("TWEET MESSAGE!")
print("TWITTER FOR?")
tweet = input("Conjure Up A Tweet: ")

api.update_status(status = (tweet))
print('Done!')
