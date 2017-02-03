from commondefs import *

PRIMARY_ID_INDEX="0"
COMMENT_ID_INDEX="1"

HEAVY = ["damn","fuck","god","hell","jesus","shit"]
LIGHT = ["dang","darn","flip","fudge","gosh","heck","jeebus","jeez","shoot"]
CUSSES = HEAVY+LIGHT


#Filters a list a comments so that duplicate entries aren't stored.
#Parameters:
#   _comments: A list of Praw comment objects
#Return Value:
#   _comments: A list of Praw comment objects which have not been stored in the database
#
def filterComments(_dbConn, _comments):
    #First we get the comment ids from the database
    query = "SELECT c_id FROM "+TABLE_NAME
    curs = _dbConn.cursor()
    curs.execute(query)
    _dbConn.commit()

    #Now we collect the existing comments from the query result
    numExistingComments = int(curs.rowcount)
    existingComments = [lambda x: x[COMMENT_ID_INDEX], curs.fetchall()]

    #Check to see if any of the comments we want to insert already exist
    for c in range(len(_comments)):
        if _comments[c].id in existingComments:
            del _comments[c]

    return _comments


#Inserts a new comment entry into the database
#Parameters:
#   _comment: A praw comment object
#   _cussCounts: A dictionary relating each cuss to how many times it was used in this comment
#Return Value:
#   None
#
def insertNewComment(_dbConn, _comment, _subredditName, _cussCounts):
    curs = _dbConn.cursor()
    curs.execute("INSERT INTO "+TABLE_NAME+" (c_id,subreddit,ups,downs,controversiality,"+','.join(CUSSES)+") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
        tuple([str(_comment.id), _subredditName, _comment.ups, _comment.downs, _comment.controversiality]+[_cussCounts[CUSSES[x]] for x in range(15)]))
        #We cast _comment.id to a string because it is originally a unicode string.
        #The cuss counts are merged together with the list to ensure consistency of insertion

    #TODO: cursor.success?
    return
