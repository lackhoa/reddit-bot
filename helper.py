from typing import List
import praw
import config
import os
Conversation = List[praw.models.Comment]

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

def get_depth(cmt: praw.models.Comment) -> int:
    '''
    Return the depth of a comment tree:
    '''
    depth = -1
    level = [cmt]
    while level:
        depth += 1
        temp = []
        for c in level:
            if c.replies:
                temp.extend(c.replies)
        level = temp

    return depth

def get_level(cmt: praw.models.Comment, level: int) -> List[praw.models.Comment]:
    '''
    Get one level of a comment tree:
    Return: list of Comment object
    '''
    result = [cmt]
    for _ in range(level):
        temp = []
        for c in result:
            temp.extend(c.replies)
        result = temp

    return result

def str_conv(conv: Conversation) -> str:
    '''
    Return the string representation of a conversation
    '''
    result = ''
    counter = 0
    for cmt in conv:
        result += '|'*counter + '<#{2} (id: {3})> {0} said: {1}\n'.format(cmt.author.name, cmt.body, counter, cmt.id)
        counter += 1
    return result

def str_convs(convs: List[Conversation]) -> str:
    '''
    Return the string representation of a conversation list
    '''
    result = ''
    result += 'Found {0} conversations\n'.format(len(convs))
    for conv in convs:
        result += 'Conversation between {0} and {1} (length {2}):\n'.format(conv[0].author.name, conv[1].author.name, len(conv))
        result += str_conv(conv) + '\n'
        result += ('-' * 100) + '\n'

    return result
