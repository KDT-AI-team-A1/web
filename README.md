# Web Search

![image](https://user-images.githubusercontent.com/42461455/110324105-e311bd00-8058-11eb-97d8-b1c28e2cf846.png)

기능 구현 해두었습니다. 현재위치 기반으로 가까운 약국 및 편의점 검색 가능합니다

## WebCam Capture

1. git clone
2. python manage.py runserver
3. 127.0.0.1:8000
4. 버튼 누르면 카메라 캡쳐 후 capture_img 폴더에 저장 (얼굴 인식 or not)
5. 캡쳐는 그대로 원래 위치기반 편의점 검색으로 redirect
6. 얼굴 인식은 인식 되면 5장 캡쳐된 것 보여주기 ( 인식 안되면 그대로 멈춰있기 - 마스크 착용시 인식못함 )
   @@@ 얼굴 인식 시 놀람 주의 @@@
   얼굴 인식 아닌거는 5장 캡쳐 저장만 하고 지도 보여주기

#### 테스트 결과 :

![test](https://user-images.githubusercontent.com/42461455/110779179-928f9f00-82a6-11eb-81b1-6abf53a1f0ed.png)
