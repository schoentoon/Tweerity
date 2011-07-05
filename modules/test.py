#!/usr/bin/python2
import re

def remove_html_tags(data):
  return re.compile(r'<.*?>').sub('',data)

def tweet(api, json):
  keys = json.viewkeys()
  if 'retweeted_status' in keys:
    print "\033[93m%s%s\033[0m: %s\nretweeted by \033[93m%s\033[0m via %s at %s" % (
          " "*int(15-len(json['retweeted_status']['user']['screen_name'])),
          json['retweeted_status']['user']['screen_name'],
          json['retweeted_status']['text'].replace("\n","").replace("\r",""),
          json['user']['screen_name'],
          remove_html_tags(json['source']),
          json['created_at'])
  else:
    print "\033[93m%s%s\033[0m: %s\nvia %s at %s" % (
          " "*int(15-len(json['user']['screen_name'])),
          json['user']['screen_name'],
          json['text'].replace("\n","").replace("\r",""),
          remove_html_tags(json['source']),
          json['created_at'])

tweet.event = 'tweet'
tweet.priority = 'high'

def delete(api, json):
  print "Tweet with id %s is deleted." % (
        json['delete']['status']['id'])

delete.event = 'delete'

def dm(api, json):
  print "\033[93m%s\033[0m->\033[93m%s\033[0m: %s" % (
        json['direct_message']['sender']['screen_name'],
        json['direct_message']['recipient']['screen_name'],
        json['direct_message']['text'])

dm.event = 'direct_message'

def favorite(api, json):
  print "\033[93m%s%s\033[0m has favorited the following tweet of you: %s" % (
        " "*int(15-len(json['source']['screen_name'])),
        json['source']['screen_name'],
        json['target_object']['text'])

favorite.event = 'favorite'

def unfavorite(api, json):
  print "\033[93m%s%s\033[0m has unfavorited the following tweet of you: %s" % (
        " "*int(15-len(json['source']['screen_name'])),
        json['source']['screen_name'],
        json['target_object']['text'])

unfavorite.event = 'unfavorite'

def followed(api, json):
  print "\033[93m%s%s\033[0m has followed you." % (
        " "*int(15-len(json['source']['screen_name'])),
        json['source']['screen_name'])

followed.event = 'follow'

def list_member_added(api, json):
  print "You've added \033[93m%s\033[0m to the following list: \033[93m%s\033[0m" % (
        json['target']['screen_name'],
        json['target_object']['full_name'])

list_member_added.event = 'list_member_added'

def list_member_removed(api, json):
  print "You've removed \033[93m%s\033[0m from the following list: \033[93m%s\033[0m" % (
        json['target']['screen_name'],
        json['target_object']['full_name'])

list_member_removed.event = 'list_member_removed'

def list_user_subscribed(api, json):
  print "\033[93m%s\033[0m subscribed to \033[93m%s\033[0m" % (
        json['source']['screen_name'],
        json['target_object']['full_name'])

list_user_subscribed.event = 'list_user_subscribed'

def list_user_unsubscribed(api, json):
  print "\033[93m%s\033[0m unsubscribed to \033[93m%s\033[0m" % (
        json['source']['screen_name'],
        json['target_object']['full_name'])

list_user_unsubscribed.event = 'list_user_unsubscribed'

if __name__ == '__main__':
  print __doc__.strip()
