import tweepy
import configparser
import time

from twitter_banner_maker import BannerMaker

#config
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

#Authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

banner_count = 1

while True:
	try:
		print(f"Banner #{banner_count} in progress...")

		follower_count = len(api.get_followers())
		print(f"Current follower count: {follower_count}")

		banner = BannerMaker(follower_count)
		api.update_profile_banner("banner.png")
		
		print(f"Banner #{banner_count} uploaded!")
		
		banner_count += 1
		time.sleep(61)

	except Exception as e:
		print(f"{e}\nExiting...")
		quit()
