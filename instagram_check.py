import argparse
import datetime
from instagram.client import InstagramAPI
from utils import *
from urlparse import urlparse

parser = argparse.ArgumentParser(description='Process Instagram followers and return list of inactive users based on provided criterion')
parser.add_argument('--nDays',  type = int, default = 100,
                            help='Number of Days since last post')
parser.add_argument('--CLIENT_ID', type = str, default = None,
                           help='Instagram Client ID')
parser.add_argument('--CALL_BACK', type = str, default = None,
                           help='Instagram Client call back address')
parser.add_argument('--output', type = str, required = True, help='output file for list of users')

def compute_statistics(api):
  properties = dict()
  for use in api.user_follows()[0]:
    relationship = api.user_relationship(user_id = use.id)
    if not relationship.target_user_is_private or relationship.outgoing_status == 'follows':
      media = api.user_recent_media(user_id = use.id)
      latest_post = compute_latest_post(media[0])
      average_post = compute_average_post(media[0])
      yield {'id': use.id,'name' : use.full_name,
              'latest_post' : compute_latest_post(media[0]),
              'average_post' : compute_average_post(media[0]),
              'relationship' : relationship.outgoing_status if relationship.outgoing_status == 'follows' else "public"
               }
    else:
      yield {'id': use.id,'name' : use.full_name,
              'latest_post' : None,
              'average_post' : None,
              'relationship' : "private"
               }

def find_inactive(posts,last_post = None,average_post = None):
  #print last_post
  for data in posts:
    if data['relationship'] == 'private':
      yield (data,"no_info")
    else:
      if last_post is not None:
        if data['latest_post'] is not None:
          if data['latest_post'] > last_post:
            yield (data,'no_post')
        else:
          yield (data,'no_post')
          
      if average_post is not None:
        if data['average_post'] is not None:
          if data['average_post'] < average_post:
            yield (data,'slow_post')
        else:
          yield (data,'no_post')

if __name__ == '__main__':
  args = parser.parse_args()
  print("This program detects inactive users among those who follow you on Instagram\n")
  if args.CLIENT_ID is None:
    print("In order to use this program you should setup a client on Instagram Developer website.")
    print("This is not an App and everything runs on your local machine without transfering any information to third-party servers.")
    print("Visit following website after you logged into the website:\n https://instagram.com/developer/clients/manage/ \n, create a new client, \nEnter some web address as callback URL, this can be anything.\n'unmark 'Disable implicit OAuth'.\nand enter Client ID and the website adress entered in Instagram:")  
    cl_id= raw_input("CLIENT_ID: ")
    call_back = raw_input("Call Back: ")
  else:
  	cl_id = args.CLIENT_ID
  	call_back = args.CALL_BACK
  print("In order to access your information on Instagram please open following link: \n https://instagram.com/oauth/authorize/?client_id=%s&redirect_uri=%s&response_type=token " % (cl_id, call_back))
  print("You will be asked to provide permission to access yout information, approve. Once the Instagram website opens again a different link appears in address bar,")
  token = raw_input("Paste the new address here: ")
  frags = urlparse(token).fragment.split('=')

  if frags[0] == 'access_token':
  	token = frags[1]
  else:
  	print("There is soemthing wrong with the link")

  api = InstagramAPI(access_token = token)
  inactive = find_inactive(compute_statistics(api),last_post = datetime.timedelta(days = 100))
  import codecs
  with codecs.open(args.output,'w','utf-8') as fi:
    for inact in inactive:
      fi.write(inact[0]['name']+","+str(inact[0]['id'])+","+inact[0]['relationship']+"\n")
  print 'Done'



