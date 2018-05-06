from typing import List
import praw
import config
import os
Conversation = List[praw.models.Comment]

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

#Get ONE response from a Redditor to a comment:
def get_response_from(comment: praw.models.Comment, redditor: praw.models.Redditor) -> praw.models.Comment:
    for reply in comment.replies:
        if reply.author.name == redditor.name:
            return reply
    return None

#Return a list of conversations under a comment
#cmt: Comment
def find_conv(cmt: praw.models.Comment) -> List[Conversation]:
    #The return value
    conversation_list = []
    #The level of the conversation starter
    level_index = 0

    while level_index < get_comment_depth(cmt):
        #Get all comments in the level
        level = get_level(cmt, level_index)
        for even_starter in level:
            for odd_starter in even_starter.replies:
                #The head check and the length check
                if (even_starter.is_root or even_starter.parent().author.name != odd_starter.author.name) and get_response_from(odd_starter, even_starter.author) is not None:
                    #Now this is a conversation:
                    cmt = get_response_from(odd_starter, even_starter.author)
                    conversation = [even_starter, odd_starter, cmt]
                    #The tail check:
                    while get_response_from(cmt, cmt.parent().author) is not None:
                        cmt = get_response_from(cmt, cmt.parent().author)
                        conversation.append(cmt)
                    conversation_list.append(conversation)
        level_index += 1
    
    return conversation_list

def find_conv_in_forest(forest: praw.models.comment_forest.CommentForest) -> List[Conversation]:
    '''
    Return a list of conversations in a comment forest
    '''
    result = []
    for cmt in forest:
        result.extend(find_conv(cmt))
    return result
