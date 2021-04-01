import base64
import json
import os
import cv2

import requests
from django.http import JsonResponse
from django.shortcuts import render

from . import settings

MAX_NM_CNT = 5  # max no mask
SEC = 10

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
        print(api_result)
        result = {}
        result['classes'] = api_result['classes']
        result['boxes'] = api_result['boxes']
        if 1 in api_result['classes']:  # 마스크 안쓴 값 (1) 이 리스트에 있을 경우
            result['msg'] = '마스크 미착용하셨습니다. 가까운 약국 및 편의점 목록 페이지로 이동합니다.'
            result['url'] = 'show_map'
            return JsonResponse(result)
        elif len(api_result['classes']) == 0:  # 아무 얼굴도 인식이 안된 경우
            result['msg'] = '얼굴 인식 불가능'
            return JsonResponse(result)
        else:  # 마스크를 썼을 경우
            result['msg'] = '마스크 착용하셨습니다.'
            return JsonResponse(result)


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
        result['boxes'] = api_result['boxes']
        result['classes'] = api_result['classes']
        return JsonResponse(result)

def savevideo(request):
    file_name = 'test1.mp4'
    global minute, context

    if request.method == "POST":
        minute = []
        file_name_path = os.path.join(settings.STATICFILES_DIRS[0], 'video/' + file_name)
        with open(file_name_path, 'wb') as f:
            f.write(request.FILES['file'].read())
    
        capture_count = video_read(file_name)

        result = []
        for i in range(capture_count):
            url = "http://3.36.161.101:8080/predictions/cascade_rcnn"
            files = open(os.path.join(settings.STATICFILES_DIRS[0], 'img/capture_img/' + 't'+ str(i) +'.jpg'), 'rb').read()
            r = requests.post(url, data= files)

            r = r.json()
            result.append(r['classes'])
            print(result)

        nnCnt, MAX_NN_CNT = 0, 2

        for i in result:
            print(minute)
            flag = False
            if 1 in i:
                nnCnt += 1
                if nnCnt >= MAX_NN_CNT:
                    nnCnt = 0
                    flag = True
            else:
                nnCnt = 0
            minute.append(flag)
        
        context = {'result': list(map(str, minute)), 'sec':SEC}
    
    if request.method == "GET":
        return render(request, 'video.html', context)


def video_read(file_name):
    path = './static/video/test1.mp4'
    cap = cv2.VideoCapture(path)
    #width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    #height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # 비디오의 초당 프레임
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    #비디오의  전체 프레임 수 
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    count = 0
    frame_sec = fps * SEC
    capture_count = 0
    frame_num=0

    while(cap.isOpened):
        cap.set(1, frame_num) 
        frame_num += frame_sec
        ret, frame = cap.read()
        if ret == False:
            break
        file_name_path = 'static/img/capture_img/t'+str(capture_count)+'.jpg'
        capture_count += 1
        cv2.imwrite(file_name_path, frame)
    cap.release()

    return capture_count