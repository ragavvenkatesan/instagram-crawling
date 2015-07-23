#!/usr/bin/python

from instagram.client import InstagramAPI
import json
import urllib2
import os
import time
from collections import deque
import pdb

import instagram_stuff as ist




def main():

    
    
    stack = deque([])
    known =[]
    visited = []
    
    # push the initial node in the stack
    
    stack.append(client.begin_user_id)
    known.append(client.begin_user_id)
    
    done = False
    collected = 0
    
    # Breadth first search from the initial user node
    while collected < max_collect_users and not done:
        
        # if you have enough access permissions
        check = int(api.x_ratelimit_remaining)
        if check > 100 :
            print "Remaining API requests " + str(api.x_ratelimit_remaining) + " of " + str(api.x_ratelimit)
        
            # visit node
            if not stack :
                print "Done with BFS from " + client.begin_user_id
                done = True
            else :
                current_user_id = stack.popleft()
                if current_user_id not in visited :
                    visited.append(current_user_id)
                    ist.visit_user(current_user_id , stack, known, edges, user_details, api , collect_media_flag = collect_media_flag, verbose=verbose)
                    collected = collected + 1

        else :
            print "Remaining API requests " + str(api.x_ratelimit_remaining) + " of " + str(api.x_ratelimit)
            print "Sleeping ..... "
            time.sleep(60)
            try:
                temp = api.user('1513623915')
            except:
                pass
            print "Awake ..... "




if __name__ == '__main__':

    max_followers = 20                   # How many followers per user to collect
    max_follows = 20                     # how many follows to collect per user
    max_bfs_add = 25                     # how many BFS edges to add per user
    max_collect_media = 100              # how many media items to be collected per person ?
    max_collect_users = 20               # how many users in all to collect.
    verbose = True                       # Don't be a silent code and keep printing stuff. 
    collect_media_flag = 2               # =2 means collect images and everything, = 1 means collect only images, = 0 means just collect information. 

    client_id = ' '          # user your client id
    client_secret = ' '      # user your client secret id
    redirect_uri = 'http://localhost'                       # user your redirect_uri
    
    # start with someone popular and usually followed by a lot of people. 
    begin_user_id = '460563723' # - Selena Gomez
    #begin_user_id = '19185689' # - Kayley Cuoco
    #begin_user_id = '1513623915' # - Ragav - Zero followers, zero following
    #begin_user_id = '18428658' # - Kim Kardashian
    #begin_user_id  = '1867327' # - Bill Gates

    # initiliaze the client
    client = ist.client_packet(client_id = client_id, client_secret = client_secret, redirect_uri = redirect_uri, begin_user_id = begin_user_id)  
    access_token = client.access_token( True )          # once you run the code first time. Reset this inside the instagram.py file and start using false flag
    api = InstagramAPI(client_id = client.client_id, client_secret = client.client_secret, access_token=access_token[0])
    # begin api first use    
    print "\n\n\n\n\n\n\n#########+++++++++=========+++++++++#########"
    print "Crawler Details :"
    tryflag = True
    while tryflag:
        try:
            user = api.user('1513623915')
            tryflag = False
        except:
            print "sleeping .. "
            print "Remaining API requests " + str(api.x_ratelimit_remaining) + " of " + str(api.x_ratelimit)
            time.sleep(60)
            print "awake .. "

    print "Initialized user :" + user.username
    print "User Id :" + user.id
    print "User Full Name: " + user.full_name
    print "Number of Images Posted : " + str(user.counts['media'])
    print "Number of Followers : " + str(user.counts['followed_by'])
    print "Number Follows: " +str(user.counts['follows'])
    print "#########+++++++++=========+++++++++#########\n\n\n\n\n\n\n"


    # open graph files
    if not os.path.exists('./userdata/'):
        os.makedirs('userdata')            
    edges = open("./userdata/edges.csv",'a')
    user_details = open ("./userdata/user_details.csv",'a')
    
    
    main()

    # close files
    
    edges.close()
    user_details.close()

