import praw 
import config
import time
import os

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
		if "dog" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():
			print("String with 'dog' found in comment " + comment.id)

			comment.reply("I also love dogs! [Here](https://i.imgur.com/W2XqgxI.gifv)"
			 + " is a cute gif of one")

			print("Replied to comment " + comment.id)

			comments_replied_to.append(comment.id)

			with open("comments_replied_to.txt", "a") as f:
				f.write(comment.id + "\n")

	print("Sleeping for 10 seconds...")
	#Sleep for 10 seconds...
	time.sleep(10)

def get_saved_comments():
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt", "r") as f:
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = list(filter(None, comments_replied_to))
			
	return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()
print(comments_replied_to)

while True:
	run_bot(r)