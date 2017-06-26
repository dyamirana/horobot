#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import os
import logging
import settings
import traceback
import time
import __builtin__
logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.DEBUG, filename = u'bot.log')

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    def dic(self):
        return dict


class DB:
    def __init__(self, name):
        self.db_name = name
        try:
            pass
    #         with sqlite3.connect(os.path.dirname(__file__) + os.sep + 'databases' + os.sep + name + '.db') as con:
    #             if name == 'users':
    #                 cur = con.cursor()
    #                 cur.execute(
    #                     '''CREATE TABLE IF NOT EXISTS {}
    #     (
    # user_id INT PRIMARY KEY,
    # member BOOLEAN,
    # date INT,
    # subscription INT,
    # data1 INT,
    # data2 TEXT,
    # data3 TEXT
    #     );'''.format(name))
        except:
            if settings.debug: print u'Error in utils: trying connect to db\n'+traceback.format_exc()+'\n'
            logging.error(u'Error in utils: trying connect to db\n'+traceback.format_exc()+'\n')



    def find_user(self,req):
        try:
            with sqlite3.connect(os.path.dirname(__file__) + os.sep + 'databases' + os.sep + self.db_name + '.db') as con:
                cur = con.cursor()
                cur.execute('''SELECT * FROM {} WHERE {}'''.format(self.db_name,req))
                return cur.fetchall()
        except:
            if settings.debug: print u'Error in utils: find_user\n'+traceback.format_exc()+'\n'
            logging.error(u'Error in utils\n'+traceback.format_exc()+'\n')
            return []

    def insert_user(self,id,req={}):
        try:
            ufd = self.find_user(req='user_id = '+str(id))
            if len(ufd) >0:
                ufd = ufd[0]
                default= {'member':ufd[1],'date':ufd[2],'subscription':ufd[3],'data1':ufd[4],'data2':ufd[5],'data3':ufd[6]}
            else:
                default = {'member':True,'date':time.time(),'subscription':1,'data1':0,'data2':'','data3':''}
            for i in req.keys():
                default[i] = req[i]
            req = default

            with sqlite3.connect(os.path.dirname(__file__) + os.sep + 'databases' + os.sep + self.db_name + '.db') as con:
                cur = con.cursor()
                return cur.execute('''INSERT OR REPLACE INTO '''+self.db_name+''' (user_id, member, date, subscription, data1, data2, data3) values (?,?,?,?,?,?,?);''',(id,req['member'],req['date'],req['subscription'],req['data1'],req['data2'],req['data3']))
        except:
            if settings.debug: print u'Error in utils\n'+traceback.format_exc()+'\n'
            logging.error(u'Error in utils\n'+traceback.format_exc()+'\n')
            return []

    def count(self,req=''):
        with sqlite3.connect(os.path.dirname(__file__) + os.sep + 'databases' + os.sep + self.db_name + '.db') as con:
            cur = con.cursor()
            if req !='':
                cur.execute('''SELECT Count(*) FROM {}'''.format(self.db_name)+' '+req)
            else:
                cur.execute('''SELECT Count(*) FROM {} WHERE member >0'''.format(self.db_name))
            return cur.fetchall()[0][0]

def getusers(id=None):
    if len(__builtin__.users) <1:
        return []
    if id is not None:
        returnusers = []
        users = __builtin__.users
        for i in users:
            if i['id'] == id:
                returnusers.append(i)
        return returnusers
    else:
        return __builtin__.users

def insert_users(id,**kwargs):
    user_data_dict = {'id': id}
    user_data_dict.update(kwargs)
    for i in __builtin__.users:
        if i['id'] == id:
            i.update(user_data_dict)
            return
    __builtin__.users.append(user_data_dict)



