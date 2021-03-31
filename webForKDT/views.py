import base64
import json
import os

import requests
from django.http import JsonResponse
from django.shortcuts import render

from . import settings

MAX_NM_CNT = 2  # max no mask

URL_PREFIX = "http://3.36.161.101:8080/predictions"
PROJ_MODELS = {1: 'faster_rcnn', 2: 'cascade_rcnn'}


def index(request):
    return render(request, 'index.html')


def show_map(request):
    return render(request, 'show_map.html')


def check_no_mask(request):
    """
    PROJECT 1
    마스크 착용 여부 체크(비동기 POST 요청 처리)
    :param request:
    :return: json
    """
    proj_num = 1
    if request.method == "POST":
        # 이미지 받는 부분
        post_data = json.loads(request.body)
        imgdata = base64.b64decode(post_data['imageString'][22:])

        # API로 이미지를 보내서 응답을 받는 부분
        url = '/'.join([URL_PREFIX, PROJ_MODELS[proj_num]])
        response = requests.post(url, data=imgdata)

        # 받은 응답을 파싱하여 결과 분류
        api_result = response.json()
        if 1 in api_result['classes']:  # 마스크 안쓴 값 (1) 이 리스트에 있을 경우
            return JsonResponse({'msg': '마스크 미착용하셨습니다. 가까운 약국 및 편의점 목록 페이지로 이동합니다.', 'url': 'show_map'})
        elif len(api_result['classes']) == 0:  # 아무 얼굴도 인식이 안된 경우
            return JsonResponse({'msg': '얼굴 인식 불가능'})
        else:  # 마스크를 썼을 경우
            return JsonResponse({'msg': '마스크 착용'})


def alert_no_mask(request):
    """
    PROJECT 2
    마스크 미착용 안내 방송(비동기 POST 요청 처리)
    :param request:
    :return: JSON
    """
    proj_num = 2
    if request.method == "POST":
        # 이미지 받는 부분
        post_data = json.loads(request.body)
        imgdata = base64.b64decode(post_data['imageString'][22:])

        # API로 이미지를 보내서 응답을 받는 부분
        url = '/'.join([URL_PREFIX, PROJ_MODELS[proj_num]])
        response = requests.post(url, data=imgdata)

        # 받아온 응답을 파싱해서 렌더링하는 부분
        api_result = response.json()

        global MAX_NM_CNT
        result = {'isAlert': False}

        nm_cnt = request.session.get('nm_cnt', 0)

        # 마스크 미착용 시 +1 / 최대 횟수 달성 시 안내 방송 / 모두 착용 시 초기화
        if 1 in api_result['classes']:
            nm_cnt += 1
            if nm_cnt >= MAX_NM_CNT:
                nm_cnt = 0
                result['isAlert'] = True
        else:
            nm_cnt = 0

        request.session['nm_cnt'] = nm_cnt

        result['nm_cnt'] = nm_cnt
        result['nm_cntMax'] = MAX_NM_CNT
        return JsonResponse(result)


def savevideo(request):
    if request.method == "POST":
        file_name_path = os.path.join(settings.STATICFILES_DIRS[0], 'img/capture_img/test1.mp4')
        with open(file_name_path, 'wb') as f:
            f.write(request.FILES['file'].read())
    return render(request, 'index.html')
