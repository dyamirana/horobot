# -*- coding: utf-8 -*-
import os
import urlparse

if 'appname' in os.environ:
    host = 'https://'+os.environ.get('appname')+'.herokuapp.com'
else:
    host = 'http://vps.kadabot.tk'
group_id=int(os.environ.get('groupid',141410969))

token = os.environ.get('token','740f3f24062cf595ba12a8e5862c270814f4a5d7d7ab2a4001c5c45438d1881dea2d3d79124b4d0b670aa')
debug=True
db=False
dispatch=True
dispatch_timer=5

reposter_type='full_repost'
repost_tag=u'#рассылка'

join = True
join_mes=u'Привет!'

joinpls=u'Вступи в группу чтобы получить свой гороскоп'

leave = True
leave_mes=u'Пока!'

