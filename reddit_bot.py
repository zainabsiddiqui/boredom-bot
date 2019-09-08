import praw 
import config
import time

def bot_login():
	print("Logging in...")

	r = praw.Reddit(username = config.username, 
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = "lacetrim's dog comment responder v0.1")

	print("Logged in!")

	return r

def run_bot(r):
	print("Obtaining 25 comments...")

	for comment in r.subreddit('test').comments(limit=25):
		if "dog" in comment.body:
			print("String with 'dog' found in comment " + comment.id)

			comment.reply("I also love dogs! [Here](https://i.imgur.com/W2XqgxI.gifv)"
			 + " is a cute gif of one")

			print("Replied to comment " + comment.id)

	print("Sleeping for 10 seconds...")
	
	#Sleep for 10 seconds...
	time.sleep(10)

while True:
	r = bot_login()
	run_bot(r)