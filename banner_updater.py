#!/usr/bin/python3

#TWITTER BANNER AUTOUPDATER
#BY: Susllike
#VERSION: 5.0 HOP-POP

import tweepy
import configparser
import time
import requests

from twitter_banner_maker import BannerMaker

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
			
			"""
			A bit of a crutch: the "if" prevents the first update
			from sending the message to someone who might have
			already been following me. Definitely needs rewriting.	
			"""
			if banner_count != 1:
				try:
					api.send_direct_message(
						recipient_id = my_followers[0].id,
						text = (
							"Hey there, how are you doing?\n\n" +
							"I'm glad you decided to follow me! " +
							"If there is anything you want me to " +
							"make/talk about, you can let me know. " +
							"Or you can just talk to me for any other " +
							"reason too, that's also allowed :^)\n\n" +
							"Have a great day/night/whatever time of " +
							"day it is for you at the moment.\n\n" +
							"Again, thanks for following me!\n\n" +
							"(If we already talked before - oops; " +
							"this is automated, and my code is not " +
							"the smartest. This pretty much sums up " +
							"my content :P)"
						)
					)
				except:
					print(
						"Oh well, we tried. " +
						"Don't forget to DM " +
						f"{my_followers[0].name}!"
					)

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

		"""
		Sleeping to prevent getting rate limited.
		Doing exactly 1 second was slightly unreliable,
		so it's 2 instead. Almost the same anyway.
		"""
		time.sleep(2)

		for i in range(2):
			#Line Up -> Line Clear, reduces clutter
			print("\033[1A", end = "\x1b[2K")

	except Exception as e:
		"""
		Pretty much all of the errors are non-lethal.
		So, just keep going and hope that it will sort itself out.
		"""
		print(e)
		continue

	except KeyboardInterrupt:
		#Quitting
		break

print(f"\nExiting...")
quit()
