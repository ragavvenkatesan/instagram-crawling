#!/usr/bin/python

from instagram.client import InstagramAPI
import json
import urllib2
import cv2
import imaging_stuff as image
import os
import time
import pdb






# class defined for the client stuff - standard code from instagram
class client_packet :
    
    def __init__(self, client_id, client_secret, redirect_uri, begin_user_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.begin_user_id = begin_user_id
    
    def access_token(self,flag):
        if flag:
            scope = []
            self.api = InstagramAPI(client_id = self.client_id, client_secret = self.client_secret, redirect_uri = self.redirect_uri)
            redirect_uri = self.api.get_authorize_login_url(scope = scope)

            print "Visit this page and authorize access in your browser:\n", redirect_uri

            code = raw_input("Paste in code in query string after redirect: ").strip()
            self.access_token = self.api.exchange_code_for_access_token(code)
            print self.access_token
        else:
            self.access_token = 'Insert Your actual Client Access token to not repeath this again and again'

        return self.access_token










# Visit the user node
def visit_user(user_id , stack, known, edges, user_details, api, max_followers = 20 , max_follows = 20, max_bfs_add = 20 , max_collect_media = 20, collect_media_flag = 2, verbose = False):
    
    print "\n\n\n\n\n\n\n#########+++++++++=========+++++++++#########"
    
    

    # Collect User Data
    try :
        user = api.user(user_id)

    except:
        if verbose:
            print user_id + " is private"
            print "#########+++++++++=========+++++++++#########\n\n\n\n\n\n\n"
            print "Current Stack Size : " + str(len(stack))
        
        return stack
    
    print "Initialized user :" + user.username
    print "User Id :" + user.id
    print "User Full Name: " + user.full_name
    print "Number of Images Posted : " + str(user.counts['media'])
    print "Number of Followers : " + str(user.counts['followed_by'])
    print "Number Follows: " +str(user.counts['follows'])
    
    nodes = open("./userdata/nodes_known.csv",'a')
    nodes.write(user.id + "\n")
    nodes.close()

    user_details.write(user.id + "," + user.username + "," + user.full_name.encode("utf-8","ignore") + "," + str(user.counts['media']) + "," + str(user.counts['followed_by']) + "," + str(user.counts['follows']) + ",")

    if not os.path.exists('./profilepictures'):
        os.makedirs('profilepictures')
    #  Collect the User Profile Picture and popularity of profile picture
    if collect_media_flag > 0:
        image.download_image(user.profile_picture,"./profilepictures/" + user.id + ".jpg")
        mit_api = urllib2.urlopen('http://popularity.csail.mit.edu/cgi-bin/image.py?url=' + user.profile_picture) # collect mit popularity score.
        mitoutput = json.load(mit_api)
        user_details.write(str(mitoutput['popscore'])  + "\n")
    else:
        user_details.write("\n")

    # Show User Profile Picture

    if verbose and collect_media_flag > 0:
        profile_picture = cv2.imread("./profilepictures/" + user.id + ".jpg")
        cv2.imshow(user.full_name,profile_picture)
        cv2.waitKey(1)

    # Collect user's graph neighborhood - follows
    tryflag = True
    while tryflag :
        try:
            follows, pagination = api.user_follows(user.id)
            tryflag = False
        except :
            print "Sleeping ... "
            print "Remaining API requests " + str(api.x_ratelimit_remaining) + " of " + str(api.x_ratelimit)
            time.sleep(60)
            print "Awake .. "

    while pagination and len(follows) < max_follows:
        tryflag = True
        while tryflag :
            try :
                current_list, pagination = api.user_follows(with_next_url = pagination)
                follows.extend(current_list)
                tryflag = False
            except :
                print "Sleeping ..."
                print "Remaining API requests " + str(api.x_ratelimit_remaining) + " of " + str(api.x_ratelimit)
                time.sleep(60)
                print "Awake .. "
    


    # Collect user's graph neighborhood - followed by
    tryflag = True
    while tryflag:
        try :
            followed_by, pagination = api.user_followed_by(user.id)
            tryflag = False
        except :
            print "Sleeping ..."
            print "Remaining API requests " + str(api.x_ratelimit_remaining) + " of " + str(api.x_ratelimit)
            time.sleep(60)
            print "Awake .. "

    while pagination and len(followed_by) < max_followers:
        tryflag = True
        while tryflag:
            try:
                current_list, pagination = api.user_follows(with_next_url = pagination)
                followed_by.extend(current_list)
                tryflag = False
            except:
                print "sleeping ..."
                print "Remaining API requests " + str(api.x_ratelimit_remaining) + " of " + str(api.x_ratelimit)
                time.sleep(60)
                print "awake .. "

    count = 0
    nodes = open("./userdata/found_nodes.csv",'a')
    for edge in followed_by:
        edges.write(edge.id + "," + user.id + "\n")
        if edge.id not in known:
            if count < max_bfs_add:
                stack.append(edge.id)
                count = count + 1
            known.append(edge.id)
            nodes.write(edge.id + "\n")

    count = 0
    for edge in follows:
        edges.write(user.id + "," + edge.id + "\n")
        if edge.id not in known:
            if count < max_bfs_add:
                stack.append(edge.id)
                count = count + 1
            known.append(edge.id)
            nodes.write(edge.id + "\n")


    nodes.close()


    if verbose:
        print "Number of Followers of " + user.full_name + " crawled : " + str(len(followed_by))


    #  Collect the user Media
    if collect_media_flag > 0:
        collect_media(user, api, max_collect_media, collect_media_flag, verbose)
    
    if verbose:
        print "Finished Visiting user : " + user.full_name

    print "#########+++++++++=========+++++++++#########\n\n\n\n\n\n\n"



    print "Current Stack Size : " + str(len(stack))

    cv2.destroyAllWindows()














# Collect and store iamges
def collect_media(user, api , max_collect_media, flag, verbose = False ):


    print "Collecting Media Of : " + user.full_name

    tryflag = True
    while tryflag :
        try :
            media_list, pagination = api.user_recent_media(user_id = user.id, count = max_collect_media)
            tryflag = False
        except :
            print "sleeping .."
            print "Remaining API requests " + str(api.x_ratelimit_remaining) + " of " + str(api.x_ratelimit)
            time.sleep(60)
            print " awake..."
    
    while pagination and len(media_list) < max_collect_media:
        tryflag = True
        while tryflag:
            try:
                current_list, pagination = api.user_recent_media(with_next_url = pagination)
                media_list.extend(current_list)
                tryflag = False
            except:
                print "sleeping .."
                print "Remaining API requests " + str(api.x_ratelimit_remaining) + " of " + str(api.x_ratelimit)
                time.sleep(60)
                print " awake..."

    print "Number of Photo Information Acquired From " + user.full_name + " is : " + str(len(media_list))

    if not os.path.exists("./media/" + user.id):
        os.makedirs("./media/" + user.id)


    f = open("./media/" + user.id + "/data.csv",'w')

    count = 0
    for media in media_list:
        if media.type == "image":
            current_url = media.get_standard_resolution_url()
            
            if flag == 2:
                image.download_image(current_url, "./media/" + user.id + "/image_" + str(count) + ".jpg")
            mit_api = urllib2.urlopen('http://popularity.csail.mit.edu/cgi-bin/image.py?url=' + current_url)
            mitoutput = json.load(mit_api)
            
            if media.caption:
                f.write(str(count) + "," + str(media.like_count) + "," + str(media.comment_count) + "," + str(mitoutput['popscore']) + "," + media.filter + "," + media.id + "," + current_url + "," + media.caption.text.encode("utf-8","ignore").replace("/n"," ") + "\n")
            else:
                f.write(str(count) + "," + str(media.like_count) + "," + str(media.comment_count) + "," + str(mitoutput['popscore']) + "," + media.filter + "," + media.id + "," + current_url + "\n")
            

            
            
            if verbose and flag == 2:
                current_image = cv2.imread("./media/" + user.id + "/image_" + str(count) + ".jpg")
                cv2.imshow(user.username, current_image)
                
                print "For image " + str(count) + " Number of Likes  = " + str(media.like_count) + " Number of Comments = " + str(media.comment_count) + " and MIT popularity score = " + str(mitoutput['popscore'])
                if media.caption:
                    print "Caption of the Image : " + media.caption.text
            
            cv2.waitKey(1)
            count = count + 1

    if verbose:
        print "Number of Photos Downloaded from" + user.full_name + " is : " + str(count)
        f.close()


    cv2.destroyAllWindows()



