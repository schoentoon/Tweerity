#!/usr/bin/env python
import sys, os, re, threading, imp
import twitter
import signal

home = os.getcwd()

class Tweerity(twitter.Bot): 
  def __init__(self, config):
    twitter.Bot.__init__(self, config.access_key, config.access_secret, config.screen_name)
    self.config = config
    self.stats = {}
    self.setup()
    signal.signal(signal.SIGHUP, self.setup)

  def setup(self, signum=1, frame=None): 
    self.variables = {}
    filenames = []
    if not hasattr(self.config, 'enable'): 
      for fn in os.listdir(os.path.join(home, 'modules')): 
        if fn.endswith('.py') and not fn.startswith('_'): 
          filenames.append(os.path.join(home, 'modules', fn))
    else: 
      for fn in self.config.enable: 
        filenames.append(os.path.join(home, 'modules', fn + '.py'))
    if hasattr(self.config, 'extra'): 
      for fn in self.config.extra: 
        if os.path.isfile(fn): 
          filenames.append(fn)
        elif os.path.isdir(fn): 
          for n in os.listdir(fn): 
            if n.endswith('.py') and not n.startswith('_'): 
              filenames.append(os.path.join(fn, n))
    modules = []
    excluded_modules = getattr(self.config, 'exclude', [])
    for filename in filenames: 
      name = os.path.basename(filename)[:-3]
      if name in excluded_modules:
        continue
      try:
        module = imp.load_source(name, filename)
      except Exception, e: 
        print >> sys.stderr, "Error loading %s: %s (in bot.py)" % (name, e)
      else: 
        if hasattr(module, 'setup'): 
          module.setup(self)
        self.register(vars(module))
        modules.append(name)
    if modules: 
      print >> sys.stderr, 'Registered modules:', ', '.join(modules)
    else:
      print >> sys.stderr, "Warning: Couldn't find any modules"
      sys.exit(1)
    self.bind_commands()

  def register(self, variables):
    for name, obj in variables.iteritems():
      if hasattr(obj, 'event'): 
        self.variables[name] = obj

  def bind_commands(self): 
    self.commands = {'high': [], 'medium': [], 'low': []}

    def bind(self, priority, func): 
      print priority, func.event, func
      if not hasattr(func, 'name'): 
        func.name = func.__name__
      if func.__doc__: 
        if hasattr(func, 'example'): 
          example = func.example
        else:
          example = None
      self.commands[priority].append(func)

    for name, func in self.variables.iteritems():
      if not hasattr(func, 'priority'): 
        func.priority = 'medium'

      if not hasattr(func, 'thread'): 
        func.thread = True

      if not hasattr(func, 'event'):
        func.event = 'tweet'

      bind(self, func.priority, func)

  def call(self, func, api, json):
    try:
      func(api, json)
    except Exception, e: 
      print e

  def dispatch(self, api, json):
    keys=json.viewkeys()
    if 'event' in keys:
      if json['event'] == 'follow':
        if json['source']['screen_name'] == self.config.screen_name:
          self.friends.append(json['target']['id'])
    if "friends" not in keys:
      if 'event' in keys:
        events = [json['event']]
      elif 'direct_message' in keys:
        events = ['direct_message']
      elif 'delete' in keys:
        events = ['delete']
      else:
        events = ['tweet']
        if 'retweeted_status' in keys:
          if ("@%s" % (self.config.screen_name)).lower() in json['retweeted_status']['text'].lower():
            events.append('mention')
        elif 'text' in keys:
          if ("@%s" % (self.config.screen_name)).lower() in json['text'].lower():
            events.append('mention')
        if 'tweet' in events and 'mention' not in events:
          events.append('nomention')
      for priority in ('high', 'medium', 'low'):
        for func in self.commands[priority]:
          if func.event in events:
            if func.thread:
              threading.Thread(target=self.call, args=(func, api, json)).start()
            else:
              self.call(func, api, json)
    else:
      for i in json["friends"]:
        self.friends.append(i)

if __name__ == '__main__': 
   print __doc__
