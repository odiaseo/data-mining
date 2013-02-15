'''
Created on Feb 5, 2013

@author: Pele Odiase
'''
from bs4 import BeautifulSoup
import HTMLParser
import networkx as nx
import sys
import os
import urllib2

if len(sys.argv) > 1:
    URL = sys.argv[1]
else:
    URL = "http://ajaxian.com"
    
if len(sys.argv) > 2:
    MAX_DEPTH = int(sys.argv[2])
else:
    MAX_DEPTH = 1
    
XFN_TAGS = set([
    'colleague',
    'sweetheart',
    'parent',
    'co-resident',
    'co-worker',
    'muse',
    'neighbor',
    'sibling',
    'kin',
    'child',
    'date',
    'spouse',
    'me',
    'acquaintance',
    'met',
    'crush',
    'contact',
    'friend',
])
 

        
OUT = "../data/graph.dot"
depth = 0

g = nx.DiGraph()  

next_queue = [URL]

while depth < MAX_DEPTH :
    depth += 1
    (queue, next_queue) = (next_queue, [])
    
    for item in queue:
        try:
            page = urllib2.urlopen(item)
        except:
            print 'Failed to fetch ' + item
            continue
        
        try:
            soup = BeautifulSoup(page)
        except:
            print 'Failed to parse ' + item  
            
            
        anchorTags = soup.findAll('a')
        
        if not g.has_node(item):
            g.add_node(item)
    
        for a in anchorTags:
            if a.has_key('rel'):
                if len(set(a['rel']) & XFN_TAGS) > 0:
                    tag = a['rel']
                    friend_url = a['href']
                    g.add_edge(item, friend_url)
                    g[item][friend_url]['label'] = tag[0].encode('utf-8')
                    g.node[friend_url]['label'] = a.contents[0].encode('utf-8')
                    
                    next_queue.append(friend_url)     

try:
    nx.drawing.write_dot(g, OUT)
    cmd = "circo -Tpng -Ograph " + OUT    
    os.system(cmd)
except IOError as e:
    print "unable to scrape data {0} -> {1}".format(e.errno, e.strerror)
else:
    print "graph created successfully"
    print g.number_of_edges()
    print g.number_of_nodes()

 
    
