from django.shortcuts import render
import cv2

# Create your views here.

def index(request):
    webCapture()

    return render(request, 'show_map.html')

def webCapture():
    cap = cv2.VideoCapture(0)

    while(True):
        ret, frame = cap.read()
        cv2.imshow('frame_color', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return