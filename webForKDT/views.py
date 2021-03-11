from django.shortcuts import render
import cv2
import numpy as np

def index(request):
    return render(request, 'index.html')

def webCapture1(request):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    count = 0

    while True:
    # 카메라로 부터 사진 1장 얻기 
        ret, frame = cap.read()
        count += 1
        file_name_path = 'static/img/capture_img/test'+str(count)+'.png'
        cv2.imwrite(file_name_path,frame, params=[cv2.IMWRITE_PNG_COMPRESSION,0])

        if count==5:
            break

    cap.release()
    cv2.destroyAllWindows()

    return render(request, 'show_map.html')

def webCapture(request):
    # 카메라 실행 
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    count = 0
    not_found = 0

    while True:
    # 카메라로 부터 사진 1장 얻기 
        ret, frame = cap.read()
        # 얼굴 감지하여 얼굴만 가져오기 
        if face_extractor(frame) is not None:
            count+=1
            # 얼굴 이미지 크기를 200x200으로 조정 
            face = cv2.resize(face_extractor(frame),(200,200))
            # capture_img 폴더에 png 파일로 저장 
            file_name_path = 'static/img/capture_img/test'+str(count)+'.png'
            cv2.imwrite(file_name_path,face)
            
            #화면에 얼굴과 현재 저장 개수 표시
            cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.imshow('Face Cropper',face)
        else:
            print("Face not Found")
            not_found+=1
            if not_found > 100:
                break
            pass

        if count==5:
            break

    cap.release()
    cv2.destroyAllWindows()

    if count != 5:
        return render(request, 'index.html')

    return render(request, 'face_rec.html')

#전체 사진에서 얼굴 부위만 잘라 리턴
def face_extractor(img):
    # 얼굴 인식용 xml 파일 
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # 흑백처리 
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # 얼굴 찾기 
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    # 찾은 얼굴이 없으면 None으로 리턴 
    if faces is():
        return None
    # 얼굴들이 있으면 
    for(x,y,w,h) in faces:
        cropped_face = img[y:y+h, x:x+w]
    # cropped_face 리턴 
    return cropped_face