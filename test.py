import praw
import config
import os

#Create a reddit instance
def bot_login():
    r = praw.Reddit(username = config.username,
        password = config.password,
        client_id = config.client_id,
        client_secret = config.client_secret,
        user_agent = "lackhoa1's cat comment responder")
    return r

#Get a comment link from a comment object
def get_comment_link(comment):
    return "http://www.reddit.com/r/{0}/comments/{1}/_/{2}".format(comment.submission.subreddit, comment.submission, comment.id)

#Find curse words in a comment tree and return a list of those comments
def find_cmt_with_curse(comments):
    result = []
    for comment in comments:
        if "fuck" in comment.body or "shit" in comment.body:
            result.append(comment)
    return result

#The "main loop"
def run_bot(r):
    for cmt in r.submission(id = '8fhz8v').comments.list():
        print(get_comment_link(cmt))

#Create a Reddit instance
r = bot_login()
#Do the stuffs with the instance
run_bot(r)
