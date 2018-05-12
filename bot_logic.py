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
        try:
            rep_name = reply.author.name
        except AttributeError:
            print('Comment has no author: {0}'.format(reply.id))
        compare_name = redditor.name
        if rep_name == compare_name:
            return reply
    return None

def find_conv(root: praw.models.Comment) -> List[Conversation]:
    '''
    Return a list of conversations under a comment
    :param root: The root comment to find conversation
    '''
    #The return value
    conversation_list = []
    #The level of the conversation starter
    level_index = 0
    depth = get_depth(root)
    while level_index < depth - 1:
        #Get all comments in the level
        level = get_level(root, level_index)
        for even_starter in level:
            if even_starter.author is None: # Deleted comments cannot be conversation starters
                continue
            for odd_starter in even_starter.replies:
                if odd_starter.author is None: # Deleted comments cannot be odd starters
                    continue
                #The head check and the length check
                if (even_starter.is_root or even_starter.parent().author is None or even_starter.parent().author.name != odd_starter.author.name) and get_response_from(odd_starter, even_starter.author) is not None:
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
