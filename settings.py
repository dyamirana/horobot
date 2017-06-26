# -*- coding: utf-8 -*-
import os
import urlparse

if 'appname' in os.environ:
    host = 'https://'+os.environ.get('appname')+'.herokuapp.com'
else:
    host = 'http://vps.kadabot.tk'
group_id=os.environ.get('groupid')

token = os.environ.get('token','')
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

