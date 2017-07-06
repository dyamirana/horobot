import logging
import traceback
import settings
import vk
import utils
from random import randint
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'bot.log')
class Functions:
    def __init__(self,api):
        self.api = api
        self.pubapi=vk.API(vk.Session(access_token='083a5837083a583708657de735086fac9f0083a083a583750f2072e9bdc2096b3522ed0'), v=5.65, timeout=30,lang=0)


    def send_message(self,user_id=None,message='',attachments=[],user_ids=[],forward=None,sticker_id=None):
        try:
            mesid = 0
            if len(attachments)>0:
                atch = []
                atch_string=''
                for i in attachments:
                    if 'access_key' in i:
                        atch.append('%s%d_%d_%s'%(i['attype'],i['owner_id'],i['id'],i['access_key']))
                    else:
                        atch.append('%s%d_%d' % (i['attype'], i['owner_id'], i['id']))
            else:
                atch=[]
            if sticker_id==None:
                if user_id==None:
                    mesid = self.api.messages.send(user_ids=','.join(str(x) for x in user_ids),message=message,forward_messages=forward,attachment=','.join(atch),random_id=randint(1,9999))
                elif user_ids==[]:

                    mesid = self.api.messages.send(user_id=user_id, message=message,forward_messages=forward, attachment=','.join(atch),random_id=randint(1, 9999))
            else:
                if user_id==None:
                    mesid = self.api.messages.send(user_ids=','.join(str(x) for x in user_ids),sticker_id=sticker_id,random_id=randint(1,9999))
                elif user_ids==[]:
                    mesid = self.api.messages.send(user_id=user_id, sticker_id=sticker_id,random_id=randint(1, 9999))

            return mesid
        except Exception as exp:
            if u'users without permission' in str(exp):
                utils.insert_users(id=user_id,messallow=0)
                return
            if settings.debug==True: print u'Error in api.func.send_message\n'+traceback.format_exc()+'\n'
            logging.error(u'Error in api.func.send_message\n'+traceback.format_exc()+'\n')
            return 0

    def whatname(self,id,type=1,case='nom'):
        try:
            name = self.pubapi.users.get(user_ids=id,name_case=case)[0]
            if type==1:
                return name['first_name']
            elif type==2:
                return  name['last_name']
            elif type==3:
                return [name['first_name'],name['last_name']]
        except:
            if settings.debug==True: print u'Error in api.func.send_message\n'+traceback.format_exc()+'\n'
            logging.error(u'Error in api.func.whatname\n'+traceback.format_exc()+'\n')
            return ''
