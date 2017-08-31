import requests
from urllib.parse import urlencode
import xmltodict
import time

def send_fcm(title):
    print(title)

if __name__ == '__main__':
    url = 'http://newsky2.kma.go.kr/service/WetherSpcnwsInfoService/WeatherWarningList?'
    f= open('keys.txt')
    param = {
        'ServiceKey': f.readline(),
        'stnId': '143',
        'fromTmFc': '20170101'}

    pre = [{'tmSeq': '0', 'title': 'FIRST'}]

    while True:
        param['toTmFc'] = time.strftime('%Y%m%d', time.localtime())
        query_params = urlencode(param, safe='%')
        r = requests.get(url + query_params)
        current = xmltodict.parse(r.text)['response']['body']['items']['item']
        for i in current:
            print(i)
            if int(i['tmSeq']) > int(pre[0]['tmSeq']):# and '풍랑' in i['title'] and '발표' in i['title']:
                send_fcm(i['title'])
        pre = current
        print()

        time.sleep(60)

