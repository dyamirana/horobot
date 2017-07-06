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
        if settings.db:
            self.db = utils.DB('users')

    def join(self,user):
        try:
            if settings.join:
                user_id = user.user_id
                if settings.db:
                    self.db.insert_user(id=user_id,req={'date':time.time()+settings.dispatch_timer,'data2':'day1','subscription':1})
                else:
                    utils.insert_users(id=user_id,member=1,mesallow=0,time=0)
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
                if settings.db:
                    self.db.insert_user(id=user_id,req={'date':time.time()+settings.dispatch_timer,'member':0})
                else:
                    utils.insert_users(id=user_id,member=0,mesallow=0,time=0)
                if self.api.messages.isMessagesFromGroupAllowed(group_id=settings.group_id,user_id=user_id)['is_allowed'] == 1:
                    utils.insert_users(id=user_id, mesallow=1)
                    self.send_message(user_id=user_id,message=settings.leave_mes)
        except Exception as exp:
            if u'Database problems' in str(exp):
                self.leave(user=user)
