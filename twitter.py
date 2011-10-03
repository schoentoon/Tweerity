#!/usr/bin/env python
import sys, re, time, threading
import twoauth, twoauth.streaming
import signal

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
    signal.signal(signal.SIGTERM, self.stop)

  def run(self):
    s=twoauth.streaming.StreamingAPI(self.oauth)
    self.userstream=s.user()
    self.userstream.start()
    while True:
      try: status=self.userstream.pop()
      except KeyboardInterrupt:
        self.stop()
      for i in status:
        try:
          self.dispatch(self.api, i)
        except:
          pass

  def dispatch(self, api, args):
    pass

  def stop(self, signum=1, frame=None):
    print "Stopping."
    self.userstream.stop()
    self.mentions.stop()
    sys.exit(0)

def main():
  print __doc__

if __name__=="__main__": 
  main()
