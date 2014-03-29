import praw
from collections import deque
from time import sleep
import json


r = praw.Reddit("rpgMessengerBot by /r/thirdegree")

def _login():
	USERNAME = raw_input("Username?\n> ")
	PASSWORD = raw_input("Password?\n> ")
	r.login(USERNAME, PASSWORD)
	return USERNAME

done = deque(maxlen=200)

Trying = True
while Trying:
	try:
		USERNAME = _login()
		Trying = False
	except praw.errors.InvalidUserPass:
		print "Invalid Username/password, please try again."

def main():
	inbox = get_messages()
	for text,title,author_name,post_id in inbox:
		if post_id in done:
			continue
		done.append(post_id)
		print author_name
		if author_name == "nyancat":
			send_messages(title, text)
			print "sending messages"
			sleep(2)
		else:
			reply_string = 'Your command has been processed.\n\n ^This ^is ^an ^automatic ^message ^to ^enable/disable ^these ^messages ^please ^PM ^this ^bot ^with ^a ^message ^saying ^"enable/disable ^PMs"'
			users = get_users()
			if "disable" in text.lower():
				users.remove(author_name)
				r.send_message(author_name, "Disable PMs", reply_string)
				sleep(2)
			elif "enable" in text.lower():
				users.append(author_name)
				r.send_message(author_name, "Enable PMs", reply_string)
				sleep(2)
			write_users(users)
			print "changing userlist"




def get_messages():
	inbox = r.get_inbox()
	for i in inbox:
		if isinstance(i, praw.objects.Message):
			text = i.body
			title = i.subject
			author_name = i.author.name.lower()
			yield text, title, author_name, i.id


def send_messages(title, text):
	users = get_users()
	for user in users:
		r.send_message(user, title, text)
		sleep(2)

def get_users():
	try:
		with open("users") as u:
			users = json.loads(u.read())
		return list(set(users))	
	except IOError:
		with open("users", "w") as u:
			pass
		return []

def write_users(users):
	with open("users", "w+") as u:
		u.write(json.dumps(users))



while True:
	try: 
		main()
		sleep(10)
	except Exception as e:
		print e
		sleep(100)
