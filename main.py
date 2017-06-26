#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import sys
import settings
import os
import traceback
from flask import Flask, request
import utils
import requests
import time
import logging
import vkcallbacklib
import __builtin__

import datetime as dt
__builtin__.users = []
# logging initial
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'bot.log')

# flask init
server = Flask(__name__)

# vk init
if settings.token is not None and settings.group_id is not None:
    vk = vkcallbacklib.callback(
        token=settings.token,
        group_id=settings.group_id)
    vkapi = vk.vkapi()
else:
    print 'Fill token and group id in settings'
    sys.exit(1)
@vk.exp_handler(string='database')
def dbproblem(exp):
    print 'suka'
    return 'continue'

# set callback server
def set_callback(url=settings.host+'/vkbot'):
    while True:
        code = vk.set_callback(server=url,group_id=settings.group_id)['state_code']
        if code == 1:
            print 'Callback installed successful'
            return 'Ok'
        elif code == 2:
            print 'Waiting for callback'
            time.sleep(5)
            continue
        elif code == 3:
            print 'Server returned incorrect answer'
            return 'Server returned incorrect answer'

        elif code == 4:
            print "Can't connect to the server, check host in the settings"
            return 'Cant connect to the server, check host in the settings'

def set_settings():
    vkapi.groups.setCallbackSettings(group_id=settings.group_id,message_new=1,group_join=1,group_leave=1)
    print 'Settings installed successful'
set_settings()

# check if server url in callback setting is right
def check_server(url=settings.host,groupid=settings.group_id):
    time.sleep(5)
    server = vkapi.groups.getCallbackServerSettings(group_id=groupid)['server_url']
    if url in server:
        return
    else:
        print 'Callback server is wrong, trying to replace callback url'
        set_callback(url=settings.host + "/vkbot")

def check_users():
    #     try:
    count = len(utils.getusers())
    users = vkapi.groups.getMembers(group_id=settings.group_id)['count']


    if count < users:
        ofset = users // 1000
        if ofset == 0:
            for i in vkapi.groups.getMembers(group_id=settings.group_id)["items"]:
                utils.insert_users(id=i,member=1,time=0,mesallow=1)
        else:
            for c in range(0, ofset):
                for i in vkapi.groups.getMembers(group_id=settings.group_id, offset=ofset * 1000)["items"]:
                    utils.insert_users(id=i, member=1,time=0,mesallow=1)
                time.sleep(0.2)

check_users()



# Message answer module
try:
    import messages
    answer_vk=messages.MessageModule(vkapi).answer
    @vk.message_handler(types=['message_new'])
    def mirror(message):
        threading.Thread(target=answer_vk,args=[message]).start()
except:
    print 'Error while importing answer module'
    if settings.debug == True: print u'Error in main while importing messages module\n' + traceback.format_exc() + '\n'
    logging.error(u'Error in main while importing messages module\n' + traceback.format_exc() + '\n')

# Join and leave module
try:
    import joinleave
    jlv_vk=joinleave.JoinLeave(vkapi)
    @vk.message_handler(types=['group_join'])
    def mirror(user):
        threading.Thread(target=jlv_vk.join,args=[user]).start()
    @vk.message_handler(types=['group_leave'])
    def mirror(user):
        threading.Thread(target=jlv_vk.leave, args=[user]).start()
except:
    print 'Error while importing joinleave module'
    if settings.debug == True: print u'Error in main while importing joinleave module\n' + traceback.format_exc() + '\n'
    logging.error(u'Error in main while importing joinleave module\n' + traceback.format_exc() + '\n')

# Reposter module
# try:
#     import reposter
#     rpst=reposter.Reposter(vkapi).dispatcher
#     @vk.message_handler(types=['wall_post_new'])
#     def mirror(message):
#         threading.Thread(target=rpst,args=[message]).start()
# except:
#     print 'Error while importing reposter module'
#     if settings.debug == True: print u'Error in main while importing reposter module\n' + traceback.format_exc() + '\n'
#     logging.error(u'Error in main while importing reposter module\n' + traceback.format_exc() + '\n')



# new updates come here
@server.route("/vkbot", methods=['POST'])
def getMessagevk():
    pr = vk.insert_update(request.stream.read().decode("utf-8"))
    return pr


@server.route("/ping")
def ping():
    return 'GOOD', 200

@server.route("/vk")
def callback():

    return str(set_callback(url=settings.host+"/vkbot")), 200

# import dispatchera
if 'appname' in os.environ:
    def pinger():
        while True:
            requests.get(settings.host + "/pinger")
            time.sleep(600)

    upd_thread = threading.Thread(target=pinger)

    upd_thread.start()
try:
    print 'Bot successful started'
    threading.Thread(target=check_server).start()
    target=server.run(host="0.0.0.0", port=os.environ.get('PORT', 80),threaded=True)

except Exception as exp:
    print u'Starting server error:\n'+str(exp)
