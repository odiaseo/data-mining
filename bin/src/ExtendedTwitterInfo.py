'''
Created on Feb 14, 2013

@author: localadmin
'''
 
import twitter
import json
import sys
import time
import cPickle 
from twitter__login import login
from twitter__util import makeTwitterRequest
 
t = login();

if len(sys.argv) > 1:
    SCREEN_NAME = sys.argv[1]
else:
    SCREEN_NAME = 'peleodiase'
    
    
    
def getFriends(screen_name=None, user_id=None, friends_limit=10000):
    
    assert screen_name is not None or user_id is not None
    
    ids = []
    cursor = -1
    
    while cursor != 0 :
        params = dict(cursor=cursor)
        if screen_name is not None:
            params['screen_name'] = screen_name
        else:
            params['user_id'] = user_id
            
        response = makeTwitterRequest(t, t.friends.ids, **params)
        ids.extend(response['ids'])
        cursor = response['next_cursor']
        print >> sys.stderr, \
            'Fetched %i ids for %s ' % (len(ids), screen_name or user_id)
            
        if len(ids) >= friends_limit:
            break
    return ids;
 

if __name__ == '__main__':
    ids = getFriends(SCREEN_NAME, friends_limit=100000)
    print ids
