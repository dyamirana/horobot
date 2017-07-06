# -*- coding: utf-8 -*-
import settings
import utils
import apifunc
from plugins import hotoscope

def answers(helper,text,user_id,attachments,message):
    ### PUT UR ANSWERS HERE ###


    helper.send_message(user_id=user_id,message=hotoscope.returnHoroScope(id=user_id,zod=text.lower()))


class MessageModule:
    def __init__(self,api):
        self.api = api
        self.functions = apifunc.Functions(api)
        self.send_message = self.functions.send_message

    def answer(self,message):
        user_id = message.user_id
        mess_time = message.date
        read_state = message.read_state

        try:
            text = message.body
        except AttributeError:
            text = ''
        try:
            attachments = []
            for i in message.attachments:
                tpe = {'attype': i['type']}
                tpe.update(i[i['type']])
                attachments.append(tpe)
                del tpe
        except AttributeError:
            attachments = []
        except TypeError:
            attachments = []

        answers(self,text,user_id,attachments,message)
