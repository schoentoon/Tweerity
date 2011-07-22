#!/usr/bin/env python
import sys, re, time, threading
import twoauth, twoauth.streaming

class Bot(): 
  def __init__(self, access_key, access_secret, screen_name):
    self.access_key = access_key
    self.access_secret = access_secret
    self.oauth=twoauth.oauth('fhGWsi5X64CCGzJ7LjI9Sw',
                             'jANLXQFGVIK0qYaCfbAIziHZXfdcg6g3pGLHOkU0',
                             self.access_key,
                             self.access_secret)
    self.api=twoauth.api('fhGWsi5X64CCGzJ7LjI9Sw',
                         'jANLXQFGVIK0qYaCfbAIziHZXfdcg6g3pGLHOkU0',
                         self.access_key,
                         self.access_secret)
    self.screen_name = screen_name
    self.verbose = True
    self.sending = threading.RLock()
    self.friends = []

  def run(self):
    s=twoauth.streaming.StreamingAPI(self.oauth)
    self.userstream=s.user()
    self.userstream.start()
    self.mentions=s.filter(track=["@%s" % self.screen_name])
    self.mentions.start()
    while True:
      try: status=self.userstream.pop()
      except KeyboardInterrupt:
        self.userstream.stop()
        self.mentions.stop()
        sys.exit(0)
      for i in status:
        try:
          self.dispatch(self.api, i)
        except:
          pass
      try: status=self.mentions.pop()
      except KeyboardInterrupt:
        self.userstream.stop()
        self.mentions.stop()
        sys.exit(0)
      for i in status:
        if i['user']['id'] not in self.friends:
          try:
            self.dispatch(self.api, i)
          except:
            pass

  def dispatch(self, api, args):
    pass

def main():
  print __doc__

if __name__=="__main__": 
  main()