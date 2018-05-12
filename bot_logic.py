from typing import List
import praw
import config
import os
from helper import *
Conversation = List[praw.models.Comment]

#Create a reddit instance
def bot_login():
    r = praw.Reddit(username = config.username,
        password = config.password,
        client_id = config.client_id,
        client_secret = config.client_secret,
        user_agent = "lackhoa1's bot")
    return r

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
