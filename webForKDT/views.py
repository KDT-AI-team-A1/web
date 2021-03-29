from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import numpy as np
import requests
import json, base64, os
from . import settings

nmCnt = 0 # count no mask
MAX_NM_CNT = 2 # max no mask

def index(request):
    return render(request, 'index.html')

def show_map(request):
    if request.method == "POST":
        post_data = json.loads(request.body)
        file_name_path = os.path.join(settings.STATICFILES_DIRS[0], 'img/capture_img/test1.png')
        imgdata = base64.b64decode(post_data['imageString'][22:])

        with open(file_name_path, 'wb') as f:
            f.write(imgdata)

    # torchserve로 이미지를 보내서 응답을 받는 부분
    url = "http://3.36.161.101:8080/predictions/faster_rcnn"
    files = open(os.path.join(settings.STATICFILES_DIRS[0], 'img/capture_img/test1.png'), 'rb').read()
    r = requests.post(url, data= files)

    # 받아온 응답을 파싱해서 렌더링하는 부분
    result = r.json()
    if 1 in result['classes']:                      # 마스크 안쓴 값 (1) 이 리스트에 있을 경우
        return render(request, 'show_map.html')
    elif len(result['classes']) == 0:               # 아무 얼굴도 인식이 안된 경우
        return render(request, 'norecog.html')
    else:                                           # 마스크를 썼을 경우
        return render(request, 'alert.html')

def alert_no_mask(request):
    if request.method == "POST":
        post_data = json.loads(request.body)
        file_name_path = os.path.join(settings.STATICFILES_DIRS[0], 'img/capture_img/test2.png')
        imgdata = base64.b64decode(post_data['imageString'][22:])

        with open(file_name_path, 'wb') as f:
            f.write(imgdata)

    # torchserve로 이미지를 보내서 응답을 받는 부분
    url = "http://3.36.161.101:8080/predictions/cascade_rcnn"
    files = open(os.path.join(settings.STATICFILES_DIRS[0], 'img/capture_img/test2.png'), 'rb').read()
    r = requests.post(url, data= files)

    # 받아온 응답을 파싱해서 렌더링하는 부분
    ts_result = r.json()

    global nmCnt, MAX_NM_CNT
    result = {'isAlert': False}

    if 1 in ts_result['classes']:
        nmCnt += 1
        if nmCnt >= MAX_NM_CNT:
            nmCnt = 0
            result['isAlert'] = True
    else:
        nmCnt = 0

    result['nmCnt'] = nmCnt
    result['nmCntMax'] = MAX_NM_CNT
    return JsonResponse(result)
