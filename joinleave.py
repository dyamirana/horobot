# -*- coding: utf-8 -*-
import settings
import utils
import apifunc
import time

class JoinLeave:
    def __init__(self, api):
        self.api = api
        self.functions = apifunc.Functions(api)
        self.send_message = self.functions.send_message


    def join(self,user):
        try:
            if settings.join:
                user_id = user.user_id
                if len(utils.getusers(id=user_id)) < 1:
                    utils.insert_users(id=user_id,member=1,mesallow=0,time=0,game=0,lives=settings.lives,score=0,pics='[]',answer='')
                else:
                    utils.insert_users(id=user_id, member=1)
                if self.api.messages.isMessagesFromGroupAllowed(group_id=settings.group_id,user_id=user_id)['is_allowed'] == 1:
                    utils.insert_users(id=user_id, mesallow=1)
                    self.send_message(user_id=user_id,message=settings.join_mes)
        except Exception as exp:
            if u'Database problems' in str(exp):
                self.join(user=user)
    def leave(self,user):
        try:
            if settings.leave:
                user_id = user.user_id
                if len(utils.getusers(id=user_id)) < 1:
                    utils.insert_users(id=user_id,member=0,mesallow=0,time=0,game=0,lives=settings.lives,score=0,pics='[]',answer='')
                else:
                    utils.insert_users(id=user_id,member=0,mesallow=0)
                if self.api.messages.isMessagesFromGroupAllowed(group_id=settings.group_id,user_id=user_id)['is_allowed'] == 1:
                    utils.insert_users(id=user_id, mesallow=1)
                    self.send_message(user_id=user_id,message=settings.leave_mes)
        except Exception as exp:
            if u'Database problems' in str(exp):
                self.leave(user=user)
