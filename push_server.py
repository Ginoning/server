import requests
import xmltodict
import time
import sys
import os
import django
from urllib.parse import urlencode
from pyfcm import FCMNotification

sys.path.append('D:\shelter_run')
os.environ['DJANGO_SETTINGS_MODULE'] = 'shelter_run.settings'
django.setup()
from app_receiver.models import User

def send_fcm(title, key):
    push_service = FCMNotification(api_key=key)
    registration_ids = [str(i) for i in User.objects.all() if i is not None]

    message_title = title
    message_body = "쉘터런을 켜서 가까운 대피소로 달리세요!"
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title,
                                                  message_body=message_body)

    print(result)

if __name__ == '__main__':
    url = 'http://newsky2.kma.go.kr/service/WetherSpcnwsInfoService/WeatherWarningList?'
    f= open('keys.txt')
    param = {
        'ServiceKey': f.readline()[:-1],
        'stnId': '143',
        'fromTmFc': '20170101'}

    firebase_api_key = f.readline()

    pre = [{'tmSeq': '0', 'title': 'FIRST'}]

    while True:
        param['toTmFc'] = time.strftime('%Y%m%d', time.localtime())
        query_params = urlencode(param, safe='%')
        r = requests.get(url + query_params)
        current = xmltodict.parse(r.text)['response']['body']['items']['item']
        for i in current:
            print(i)
            if int(i['tmSeq']) > int(pre[0]['tmSeq']) and '발표' in i['title']:
                send_fcm(i['title'].split(' / ')[1], firebase_api_key)
            else:
                break
        pre = current
        print()

        time.sleep(60)

