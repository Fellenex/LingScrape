from commondefs import *

SUBREDDITS = ["wholesomememes","happy","aww","the_donald","drunk","theredpill"]

#Gets all comments from a submission
#Parameters:
#   _redConn: A praw connection to reddit
#   _postID: The submission ID of the reddit post
#Return Value:
#   submission.comments.list(): A list of praw comment objects
#
def getCommentsFromPost(_redConn, _postID):
    submission = _redConn.submission(id=_postID)
    submission.comments.replace_more(limit=0)   #loops indefinitely on nested comments

    return submission.comments.list()


#Gets _n hot submission IDs from the requested subreddit.
#Parameters:
#   _redConn: A praw connection to reddit
#   _n: An integer
#Return Value:
#   A list of praw submission objects
#
def getNPosts(_subreddit, _n):
    return [submission for submission in _subreddit.hot(limit=_n)]
