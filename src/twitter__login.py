'''
Created on Feb 14, 2013

@author: localadmin
'''
import os
import twitter

from twitter.oauth import write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance


def login():

    # Go to http://twitter.com/apps/new to create an app and get these items
    # See also http://dev.twitter.com/pages/oauth_single_token

    APP_NAME = 'Vaboose'
    CONSUMER_KEY = 'kfDLz7qZzIrVZ26njBr8jw'
    CONSUMER_SECRET = 'SOh0bEH4cbNFladR6sHDypDkaXEvlz3e4sjdONqnJjQ'
    TOKEN_FILE = 'out/twitter.oauth'

    try:
        (oauth_token, oauth_token_secret) = read_token_file(TOKEN_FILE)
    except IOError, e:
        (oauth_token, oauth_token_secret) = oauth_dance(APP_NAME, CONSUMER_KEY,
                CONSUMER_SECRET)

        if not os.path.isdir('out'):
            os.mkdir('out')

        write_token_file(TOKEN_FILE, oauth_token, oauth_token_secret)
         
    return twitter.Twitter(domain='api.twitter.com', api_version='1',
                        auth=twitter.oauth.OAuth(oauth_token, oauth_token_secret,
                        CONSUMER_KEY, CONSUMER_SECRET))

if __name__ == '__main__':
    login()