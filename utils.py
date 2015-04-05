import datetime

def compute_latest_post(media_list):
  if len(media_list) == 0:
    return None
  return datetime.datetime.now()-media_list[0].created_time
def compute_average_post(media_list):
  if len(media_list) == 0:
    return None
  return (media_list[0].created_time - media_list[-1].created_time).days/(1.0*len(media_list))
def compute_media_liked(media_list):
  if len(media_list) == 0:
    return None
  print media_list[0].get_standard_resolution_url()
  return datetime.datetime.now()-media_list[0].created_time
def compute_average_media_liked(media_list):
  if len(media_list) == 0:
    return None
  return (media_list[0].created_time - media_list[-1].created_time).days/(1.0*len(media_list))
def unfollow(api,user):
  print("removing %s" % user.id)
  #api.block_user(user.id)
