from __future__ import unicode_literals
import csv
import codecs
import json
import requests
import youtube_dl

import sys
reload(sys)
sys.setdefaultencoding('utf8')

youtube_key = "xxxxxxxxxxxxxxxxxx"
 
#
# This function takes a list of video ID's and returns their specifics
#
def send_youtube_video_request(id_list):
 
    api_url  = "https://www.googleapis.com/youtube/v3/videos?part=snippet%2CrecordingDetails%2CcontentDetails&"
    api_url += "id=%s&" % ",".join(id_list)
    api_url += "key=%s" % youtube_key
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
        
        search_results = json.loads(response.content)
        
        return search_results
 
    return None

# This function sends the channelId and date search
#
def send_youtube_channelId_request(channelId,publishedBefore,publishedAfter,token=None):
    
    # publishedBefore and publishedAfter to the api_url
    api_url  = "https://www.googleapis.com/youtube/v3/search?part=id,snippet&type=video&channelId=xxx&publishedBefore=%s&publishedAfter=%s&maxResults=50" % (publishedBefore,publishedAfter)
    
   
    api_url += "&key=%s" % youtube_key
    
    if token is not None:
        api_url += "&pageToken=%s" % token
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
    
        search_results = json.loads(response.content)       
        
        return search_results
        
    return None

def get_all_youtube_videos(channelId,publishedBefore,publishedAfter,max_total_results):
    
    video_list = []
    next_page  = None
    first_run  = True
    
    # publishedBefore and publishedAfter here
    search_results = send_youtube_channelId_request(channelId,publishedBefore,publishedAfter)
    
    print "[*] Total videos for %s - %d" % (channelId,search_results['pageInfo']['totalResults'])
    
    while next_page is not None or first_run is True:
        
        # attempt to retrieve the token, defaults to None if not present
        next_page = search_results.get("nextPageToken")
        
        if search_results is not None:
            
            id_list = []
            
            # iterate over the search results adding them to our video list
            for video_result in search_results['items']:
                
                id_list.append(video_result['id']['videoId'])
                
            # send second request to get video details
            video_results = send_youtube_video_request(id_list)
                
            video_list.extend(video_results['items'])
                
            
            print "[*] Retrieved %d results" % len(video_list)
            
            if len(video_list) >= max_total_results:
                break
 
        # ask for the next set of search results
        search_results = send_youtube_channelId_request(channelId,publishedBefore,publishedAfter)

        
        first_run = False
        
    return video_list

# This logs 


def log_results(video_list,filename):
    
    field_names = ['Video ID','Video URL','Title','Description','Publishing Date','Duration']
    
    with codecs.open(filename,"wb",encoding='utf-8') as logfile:
           
        logger      = csv.DictWriter(logfile, fieldnames=field_names)
        logger.writeheader()    
            
        for video in video_list:
                    
            
            video_result = {}
            video_result['Video ID']    = video['id']
            video_result['Video URL']   = "https://www.youtube.com/watch?v=%s" % video['id']
            video_result['Title']       = video['snippet']['title']
            video_result['Description'] = video['snippet']['description']
            video_result['Publishing Date'] = video['snippet']['publishedAt']
            video_result['Duration'] = video['contentDetails']['duration']
            
            
            print "%s" % (video['snippet']['title'])
            
            # Download videos (need to be fixed)
            #ydl_opts = {}            
           # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
              # ydl.download            
            
            
            logger.writerow(video_result)            

channelId = "xxxx" 

# variables
publishedBefore = "xxxx"
publishedAfter  = "xxxx"
safeSearch = "none"
order = "date"

filename   = "xxx.csv"

max_total_results = 300

video_list        = get_all_youtube_videos(channelId,publishedBefore,publishedAfter,max_total_results)
 
for video in video_list:
    
    print "%s => %s" % (video['snippet']['title'],video['snippet']['description'])
    print 
    print "https://www.youtube.com/watch?v=%s" % video['id']
    print "-" * 200
    
log_results(video_list,filename)
    
