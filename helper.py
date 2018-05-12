from typing import List
import praw
import config
import os
from helper import *

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

#Return the depth of a comment tree:
def get_comment_depth(cmt: praw.models.Comment) -> int:
    if cmt.replies:
        maximum = 0
        for reply in cmt.replies:
            if get_comment_depth(reply) > maximum:
                maximum = get_comment_depth(reply)
        return (maximum + 1)
    else:
        return 0

#Get one level of a comment tree:
#Return: list of Comment object
def get_level(cmt: praw.models.Comment, level: int) -> List[praw.models.Comment]:
    result = []
    if level == 0:
        return [cmt]
    else:
        if cmt.replies:
            for reply in cmt.replies:
                result.extend( get_level(reply, level-1) )
    return result

