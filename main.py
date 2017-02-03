#Looking to see the difference in score between comments with curse words, or light versions of those curse words.

import re

from commondefs import *
from dbdefs import *
from prawdefs import *

import praw
import MySQLdb


#Counts all the cusses in a piece of text, and creates a dictionary representing the counts of each.
#Parameters:
#   _redConn: A praw connection to reddit
#   _text: A string
#Return Value:
#   cussCount: A dictionary, where the keys are cusses as strings, and the values are integers.
#   None: If there were no instances of cusses, this function returns None
#
def getCussCount(_text):
    cussCount = dict()
    total=0

    for cuss in CUSSES:
        cussCount[cuss]=len(re.findall(cuss, _text.lower()))
        total+=cussCount[cuss]

    if total == 0:
        cussCount = None

    return cussCount


def main():
    #Establish a connection to the MySQL database, and the Reddit user agent
    dbConn = MySQLdb.connect(host=HOST_NAME,user=USER_NAME,passwd=PASSWORD,db=DB_NAME,port=3306)
    redConn = praw.Reddit(BOT_NAME)

    #Create the merged subreddit we will monitor
    subreddit = redConn.subreddit('+'.join(SUBREDDITS))

    #Monitor all new submissions
    #for submission in subreddit.stream.submissions():

    #Check out the hot 1000 submissions
    for submission in subreddit.hot(limit=1000):
        print submission.id
        
        currComments = getCommentsFromPost(redConn, submission.id)

        #Take out the comments that we've already saved in the database
        filteredComments = filterComments(dbConn, currComments)

        #For each unsaved comment, we want to check its contents for cusses.
        for comment in filteredComments:

            currCussCount = getCussCount(comment.body)

            #If it has cusses, then we save it to the database
            if currCussCount:
                insertNewComment(dbConn, comment, str(submission.subreddit).lower(), currCussCount)

    print "done!"

if __name__ == '__main__':
    main()
