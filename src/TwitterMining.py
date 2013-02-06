'''
Created on Feb 5, 2013

@author: Pele Odiase
'''

import cPickle
import networkx as nx
import os
import re
import sys
import twitter


def get_rt_sources(tweet):
    rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
    return [source.strip()
                for tup in rt_patterns.findall(tweet)
                    for source in tup
                        if source not in ("RT", "via") ]
    
    
if len(sys.argv) > 1:
    keyword = sys.argv[1]
else:
    keyword = "vouchers"
    
filename = "../data/" + keyword + ".pickle"
OUT = "../data/" + keyword  
try:
    if os.path.isfile(filename):
        tweets = cPickle.load(open(filename))
    else:
        twitter_search = twitter.Twitter(domain="search.twitter.com")
        
        search_results = []
        for page in range(1,6):
            search_results.append(twitter_search.search(q=keyword, rpp=20, page=page))
        
        tweets = [ r  for result in search_results for r in result['results'] ]
                
        if len(tweets):
            file = open(filename, 'wb')
            cPickle.dump(tweets, file)
            file.close()
    
    if len(tweets):
        g = nx.DiGraph()
        for tweet in tweets:
            rt_sources = get_rt_sources(tweet['text'])
            if not rt_sources: continue
            for rt_source in rt_sources:
                g.add_edge(rt_source, tweet["from_user"], {"tweet_id" : tweet["id"]})
        
        dotfile = OUT + ".dot"
        
        nx.drawing.write_dot(g, dotfile)
        cmd = "circo -Tpng -O" + OUT + " " + dotfile
        
        os.system(cmd)
        
        print g.number_of_edges()
        print g.number_of_nodes()
    
except IOError as e:
    print "unable to process twitter feeds {0} -> {1}".format(e.errno, e.strerror)
else:
    print len(tweets) ,
    print " twitter feeds processed successfully"
    