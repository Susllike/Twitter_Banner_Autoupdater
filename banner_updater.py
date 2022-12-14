#!/usr/bin/python3

#TWITTER BANNER AUTOUPDATER
#BY: Susllike
#VERSION: 5.0 HOP-POP

import tweepy
import configparser
import time
import requests

from BannerMaker import BannerMaker

#Config
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

my_handle = config['twitter']['handle']
#Authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

banner_count = 1
current_followers = 0

while True:
	try:
		"""
		User lookup can be done 60 times as much as follower count
		in the same 15-minute interval. Such speed shortens the
		time between the user following and the banner getting
		updated.
		"""
		me = api.get_user(screen_name = my_handle)
		follower_count = me.followers_count
		print(f"Current follower count: {follower_count}")
		
		if follower_count != current_followers:
			#Lookup the follower count only when I *need* to.
			my_followers = api.get_followers()
			current_followers = follower_count

			#The name for the banner
			latest_handle = my_followers[0].screen_name

			#Follower's pfp
			latest_follower = my_followers[0]._json['profile_image_url_https']
			img_url = latest_follower.replace("normal", "400x400")
			follower_pic = requests.get(img_url).content

			FILENAME = "latest_follower_pfp.jpg"
			with open(FILENAME, "wb") as file:
				file.write(follower_pic)

			#New banner with the latest follower
			banner = BannerMaker(follower_count, FILENAME, latest_handle)
			#Sending the banner to Twitter
			api.update_profile_banner("banner.png")		

			print(f"Banner #{banner_count} uploaded!")
			banner_count += 1
		else:
			print("Banner not updated.")

		time.sleep(2)

		for i in range(2):
			#Line Up -> Line Clear, reduces clutter
			print("\033[1A", end = "\x1b[2K")

	except Exception as e:
		#Pretty much all of the errors are non-lethal.
		#So, just keep going and hope that it will sort itself out.
		print(e)
		continue

	except KeyboardInterrupt:
		#Quitting
		break

print(f"\nExiting...")
quit()
