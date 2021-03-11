from django.shortcuts import render
import cv2

# Create your views here.

def index(request):
    webCapture()

    return render(request, 'show_map.html')

def webCapture():

    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    ret, frame = cam.read()
    cv2.imwrite('capture_img/test.png',frame, params=[cv2.IMWRITE_PNG_COMPRESSION,0])
    cam.release()

    return