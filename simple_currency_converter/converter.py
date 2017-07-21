import pycurl
from io import BytesIO
import datetime
import json
"""
Converts Currencies on date. Gets data from http://www.nbrb.by/API/ExRates/Rates/
Params:
amount=1;
source='BYN'
target='EUR'
date = datetime object
"""
def fetch_data(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    return json.loads(buffer.getvalue().decode('utf-8'))
def list():
    url_target = "http://www.nbrb.by/API/ExRates/Currencies"
    out =[]
    for currency in fetch_data(url_target):
        out.append({'Cur_Abbreviation':currency['Cur_Abbreviation'], 'Cur_Name_EngMulti':currency['Cur_Name_EngMulti']})
    return out
def convert(amount=1,source='BYN',target='EUR', date=datetime.datetime.now().date()):
    date_temp = date
    date = date.strftime('%Y-%m-%d')
    if date_temp > datetime.datetime.now().date():
        date = datetime.datetime.now().strftime('%Y-%m-%d')
    if target == 'BYN' and source == 'BYN':
        return amount
    elif source == 'BYN':
        url_target = 'http://www.nbrb.by/API/ExRates/Rates/{currency}?Periodicity=0&onDate={date}&ParamMode=2'.format(date=date,currency=target)
        result = fetch_data(url_target)
        rate_result = float(amount)/float(result['Cur_OfficialRate'])/float(result['Cur_Scale'])
        return rate_result
    elif target == 'BYN':
        url_target = 'http://www.nbrb.by/API/ExRates/Rates/{currency}?Periodicity=0&onDate={date}&ParamMode=2'.format(date=date,currency=source)
        result = fetch_data(url_target)
        rate_result = float(amount)*float(result['Cur_OfficialRate'])/float(result['Cur_Scale'])
        return rate_result
    else:
        url_target = 'http://www.nbrb.by/API/ExRates/Rates/{currency}?Periodicity=0&onDate={date}&ParamMode=2'.format(date=date,currency=target)
        url_source = 'http://www.nbrb.by/API/ExRates/Rates/{}?Periodicity=0&onDate={}&ParamMode=2'.format(source,date)
        out = []
        for url in [(url_target,target_rate,target), (url_source,source_rate,source)]:
            response = fetch_data(url[0])
            rate_result = response['Cur_OfficialRate']/response['Cur_Scale']
            out.append(rate_result)
        target = float(out[1])*float(amount)/float(out[0])
        return target
