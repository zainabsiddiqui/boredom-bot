import praw 
import config
import time
import os
import requests

def bot_login():

	print("Logging in...")

	# Log in to Reddit using my configuration
	r = praw.Reddit(username = config.username, 
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = "lacetrim's boredom responder v0.1")

	print("Logged in!")

	return r

def run_bot(r):

	print("Obtaining 25 comments...")

	for comment in r.subreddit('test').comments(limit=25):

		#If the comment contains a statement of boredom ("I'm bored" or "I am bored"), reply back with a random suggestion
		if ("I'm bored" in comment.body or "I am bored" in comment.body) and (comment.id not in comments_replied_to) and (comment.author != r.user.me()):

			print("String with boredom found in comment " + comment.id)

			#Append boilerplate comment with random suggestion
			comment_reply = "Oh no, there's so much you can do! Here's an idea: "
			suggestion = requests.get('http://www.boredapi.com/api/activity/').json()['activity']
			comment_reply += suggestion + ".\n&nbsp;\n\n^(Beep, boop. I am a bot. Filter my suggestions by type of activity by commenting back"
			+ "with !boredombot 'type', where type can be music, education, cooking, social, relaxation, busywork, charity, recreational, or diy. The possibilities are endless!)"

			#Reply to the comment
			comment.reply(comment_reply)
			print("Replied to comment " + comment.id)

			#Add comment id to .txt file so that we don't reply to it again
			comments_replied_to.append(comment.id)

			with open("comments_replied_to.txt", "a") as f:
				f.write(comment.id + "\n")

		elif "!boredombot" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():

				#Grab type parameter from comment
				boredom_type = comment.body.rsplit(None, 1)[-1]
				print("Found type: " + boredom_type)

				#Check if type parameter is valid
				if boredom_type in ('music', 'education', 'cooking', 'social', 'relaxation', 'busywork', 'charity', 'recreational', 'diy'):

					#Build the requests URL based on type
					comment_reply = "Fun! Here's a(n) " + boredom_type + " suggestion: "
					boredom_type_suggestion = requests.get("http://www.boredapi.com/api/activity?type=" + boredom_type).json()['activity']
					comment_reply += boredom_type_suggestion + "."

				else:

					#Error message if type is invalid
					comment_reply = "Oops, that's not a valid type/category! Valid types are music, education, cooking, social, relaxation, busywork, charity, recreational, or diy."

				#Reply to the comment
				comment.reply(comment_reply)
				print("Replied to comment " + comment.id)

				#Add commment id to .txt file so that we don't reply to it again
				comments_replied_to.append(comment.id)

				with open("comments_replied_to.txt", "a") as f:
					f.write(comment.id + "\n")

	#Sleep for 10 seconds...
	print("Sleeping for 10 seconds...")
	time.sleep(10)

def get_saved_comments():

	if not os.path.isfile("comments_replied_to.txt"):

		#If the .txt file does not exist already, create a blank one
		comments_replied_to = []

	else:

		#Otherwise read and parse the file 
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