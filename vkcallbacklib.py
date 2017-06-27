 #!/usr/bin/env python
 # -*- coding: utf-8 -*-
 # lib writen by Danya Reymakh vk.com/whoreormore
 import vk
 import json
 import logging
 import sys
 import traceback
 import utils
 import threading
 from time import sleep
 from antigate import AntiGate
 import requests
 from Queue import Queue
 exq = Queue()
 
 logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'bot.log')
 
 
 
 
 class callback:
     def __init__(self, token, apiv='5.63', timeout=30,confirmation=None,group_id=None,anti_key=None):
         self.token = token
         self.api = vk.API(vk.Session(access_token=token), v=apiv, timeout=timeout)
         self.handlers = []
         self.updates = []
         self.exps=[]
         self.confirmation = confirmation
         self.group_id = group_id
         self.anti_key = anti_key
 
     def captcha_wrapper(self, captcha_image_url):
         if self.anti_key is not None:
             if AntiGate(self.anti_key).balance()>0:
                 response = requests.get(captcha_image_url, stream=True)
                 captcha = AntiGate(self.anti_key, response.raw)
                 del response
                 return str(captcha)
             else:
                 logging.error('Anticaptcha error: zero balance')
         else:
             return None
 
     vk.Session.get_captcha_key = captcha_wrapper
 
     def vkapi(self):
         return self.vkapic(self)
     class vkapic(object):
         def __init__(self,out):
             self.out=out
         def __getattr__(self, method_name):
             return self.out.req(self, method_name,self.out)
 
     class req(object):
         __slots__ = ('_api', '_method_name', '_method_args','_out')
 
         def __init__(self, api, method_name,out):
             self._api = api
             self._method_name = method_name
             self._out = out
 
         def __getattr__(self, method_name):
 
             return self._out.req(self._api, self._method_name + '.' + method_name,self._out)
 
         def __call__(self, **method_args):
 
             while True:
                 try:
                     answ = eval('self._out.api.' + self._method_name +'(**method_args)')
                     return answ
                 except Exception as exp:
                     resume = False
                     print self._out.exps
                      for i in self._out.exps:
                          if i['string'].lower() in str(traceback.format_exc()).lower():
                              wtd_con =i['func'](traceback.format_exc())
 +                            print wtd_con
                              if 'continue' in wtd_con:
  
                                  resume = True
                             else:
 
                                 resume = False
                     if resume:
                         continue
                     else:
                         raise exp
                         break
 
 
 
     def exp_handler(self, func=None, string=''):
         def decorator(handler):
             self.exps.append({'func': handler, 'string': string})
             return handler
         return decorator
 
     def message_handler(self, func=None, types=None):
         if types is None:
             types = ['message_new']
 
         def decorator(handler):
             self.handlers.append({'func': handler, 'types': types})
             return handler
         return decorator
 
     def updater(self):
         for u in self.updates:
             for i in self.handlers:
                 if u['type'] in i['types']:
                     try:
                         i['func'](utils.dotdict(u))
                     except:
                         logging.error('Error while executing handler:\n'+str(traceback.format_exc()))
             self.updates.remove(u)
             sleep(0.1)
 
     def insert_update(self,update):
         try:
             update = json.loads(update)
         except ValueError:
             logging.error('Error while decoding update: %s \n Traceback:'+str(traceback.format_exc())+'-'*10+'\n')
 
         u_type = update['type']
         if u_type == 'confirmation':
             if self.confirmation is not None:
                 return self.confirmation
             else:
                 sleep(0.2)
                 return self.api.groups.getCallbackConfirmationCode(group_id=self.group_id)['code']
         else:
             updict = {'type': u_type, 'group_id': update['group_id']}
             updict.update(update['object'])
             self.updates.append(updict)
             threading.Thread(target=self.updater).start()
             return 'ok'
 
 
 
     def set_callback(self,server,group_id=None):
         if group_id is None:
             if self.group_id is not None:
                 group_id = self.group_id
             else:
                 raise ValueError, 'Not provided group_id'
 
         return self.api.groups.setCallbackServer(group_id=group_id,server_url=server)
 
 
 
