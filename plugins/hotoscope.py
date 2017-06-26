#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytz
import datetime
import requests
import xmltodict
import utils
import time
local_tz = pytz.timezone('Europe/Minsk')
def utc_to_local():
    local_dt = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(local_tz)
    return int(datetime.datetime.strptime(str(local_dt.date()),'%Y-%m-%d').strftime("%s"))+86400

symbols = {u'овен':'aries',u'телец':'taurus',u'близнец':'gemini',u'рак':'cancer',u'лев':'leo',u'дева':'virgo',u'весы':'libra',u'скорпион':'scorpio',u'стрелец':'sagittarius',u'козерог':'capricorn',u'водолей':'aquarius',u'рыбы':'pisces'}


def returnHoroScope(id,zod):
    if len(utils.getusers(id=id))>0:
        if utils.getusers(id=id)[0]['time'] > time.time():
            return u'Попробуйте завтра, на сегодня у Ваc уже есть предсказания'
        if zod not in symbols.keys():
            return u'Укажите точнее Ваш знак зодиака'
        r = requests.get('http://img.ignio.com/r/export/utf/xml/daily/com.xml').text
        utils.insert_users(id,time=utc_to_local())
        return xmltodict.parse(r)['horo'][symbols[zod]]['today']

