from django.http import HttpResponse

import requests
from datetime import datetime
import json

from dnd_7th_4_backend.settings.base import env
from main.models import Api9, Region


# api_9 데이터 저장을 위한 데이터 요청
def call_api_9():
    url = "http://apis.data.go.kr/1360000/LivingWthrIdxServiceV2/getSenTaIdxV2"
    #serviceKey = env('API_SERVICEKEY1')
    serviceKey = 'kRLAj2LoKpX5giQmDxfZbpmHWY8G++w0AGVsCS++Q6g6p+4ipUwMGOsXP1sduPrqOEPWjZjxqGxJjxTXzBQAsA=='
    search_date = datetime.today().strftime("%Y%m%d%H")
    print(f'api_9: get request: -----------------------------')

    now_hour = datetime.today().strftime("%H")
    region_data = Region.objects.all()
    for region in region_data:
        params = {
            "serviceKey": serviceKey,
            "areaNo": region.div_code,
            "dataType": "JSON",
            "time": "",
            "requestCode": "A41"
        }
        try:
            # api 요청
            response = requests.get(url, params=params)
            code = response.json()['response']['header']['resultCode']
            # 데이터 받기가 성공일 경우
            if code == '00':
                # API 9 데이터 저장
                today_num = "h"+str(int(now_hour)-6)
                tomorrow_num = "h"+str(int(now_hour)-6+24)
                today = response.json()['response']['body']['items']['item'][0][today_num]
                tomorrow = response.json()['response']['body']['items']['item'][0][tomorrow_num]
                div_code = response.json()['response']['body']['items']['item'][0]['areaNo']
                api_9 = Api9(today = today, tomorrow = tomorrow, div_code = div_code)
                api_9.save()
                print(f'api_9: {div_code} {today} {tomorrow} -----------------------------')

            else:
                get_api_error(str(response.status_code), response.text)

        except requests.Timeout:
            print(f'api_9: Timeout: {region.div_code}-----------------------------')
        except requests.ConnectionError:
            print(f'api_9: ConnectionError: {region.div_code}-----------------------------')

# 오전 6시마다 api_9 데이터 업데이트
def update_api_9():
    url = "http://apis.data.go.kr/1360000/LivingWthrIdxServiceV2/getSenTaIdxV2"
    #serviceKey = env('API_SERVICEKEY1')
    serviceKey = 'kRLAj2LoKpX5giQmDxfZbpmHWY8G++w0AGVsCS++Q6g6p+4ipUwMGOsXP1sduPrqOEPWjZjxqGxJjxTXzBQAsA=='
    search_date = datetime.today().strftime("%Y%m%d%H")
    print(f'api_9: get request: -----------------------------')

    now_hour = int(datetime.today().strftime("%H"))
    api9_data = Api9.objects.all()
    for api9 in api9_data:
        region = api9.div_code
        params = {
            "serviceKey": serviceKey,
            "areaNo": region,
            "dataType": "JSON",
            "time": "",
            "requestCode": "A41"
        }
        try:
            # api 요청
            response = requests.get(url, params=params)
            code = response.json()['response']['header']['resultCode']
            # 데이터 받기가 성공일 경우
            if code == '00':
                # API 9 데이터 저장
                today_num = "h"+str(now_hour-6)
                tomorrow_num = "h"+str(now_hour-6+24)
                today = response.json()['response']['body']['items']['item'][0][today_num]
                tomorrow = response.json()['response']['body']['items']['item'][0][tomorrow_num]
                api9.today = today
                api9.tomorrow = tomorrow
                api9.save()
                print(f'api_9: {region} {today} {tomorrow} -----------------------------')

            else:
                get_api_error(str(response.status_code), response.text)

        except requests.Timeout:
            print(f'api_9: Timeout: -----------------------------')
        except requests.ConnectionError:
            print(f'api_9: ConnectionError:-----------------------------')