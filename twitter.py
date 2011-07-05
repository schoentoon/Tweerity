#!/usr/bin/env python
import sys, re, time, threading
import twoauth, twoauth.streaming

class Bot(): 
  def __init__(self, access_key, access_secret):
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
    self.verbose = True
    self.sending = threading.RLock()

  def run(self):
    s=twoauth.streaming.StreamingAPI(self.oauth)
    self.streaming=s.user()
    self.streaming.start()
    while True:
      try: status=self.streaming.pop()
      except KeyboardInterrupt:
        self.streaming.stop()
        sys.exit(0)
      for i in status:
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