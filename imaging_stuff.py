
import urllib2
import pdb

def download_image(url,path_to_save):
    resource = urllib2.urlopen(url)
    output = open(path_to_save,"wb")
    output.write(resource.read())
    output.close()
