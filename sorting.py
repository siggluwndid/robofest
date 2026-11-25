import cv2
import numpy as np
import serial
import time
import glob

# ==========================================
# 1. 전역 설정 상수 (통신 속도, 쿨다운 등)
# ==========================================
BAUD_RATE = 9600
COOLDOWN_SEC = 2.5


# ==========================================
# 2. 아두이노 시리얼 연결 함수
# ==========================================
def connect_arduino():
    ports = glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyUSB*')   #glob라이브러리로 라즈베리파이에 연결된 아두이노 uno보드르 찾습니다

    for i in ports: #여러가지 포트를 찾았을 경우 포트 개수 만큼 연결을 시도합니다
        try:
            uno = serial.Serial(i, BAUD_RATE, timeout=1)    #uno라는 객체를 선언하고 그 안에 serial통신으로 찾은 포트의 이름을 넣어 연결을 시도하고, 시리얼 통신 속도를 명시합니다. 그다음 최대 대기시간을 설정하여 오류를 방지합니다.
            time.sleep(2)   #연결후 혹시모를 오류를 방지하기위하여 2초동안 작동을 정지합니다.
            print(f'{i}연결 성공!') #위의 과정을 정상적으로 마쳤다면 연결 성공 메시지를 출력합니다.
            return uno #uno객체를 반환합니다.
        except:
            print("연결 실패") #연결을 실패했을 경우에 연결 실패 메시지를 출력하고 다음 포트가 있다면 다음 포트 연결을 시도합니다.
    return None #그럼에도 연결에 실패할경우 아무것도 반환하지않고 함수를 종료합니다.

    pass


# ==========================================
# 3. 화물 판별 함수 (핵심 비전 알고리즘 영역)
# ==========================================
def classify_cargo(roi):
    """
    입력: 잘라낸 중앙 영역 이미지 (roi)
    출력: '1' (일반 화물), '2' (위험물), 또는 None (물체 없음)
    """
    # TODO (임시 테스트): BGR -> HSV 변환 후 색상 마스크 픽셀 수로 '1' 또는 '2' 판별
    # TODO (프린팅 완료 후): 위 색상 코드를 지우고 TFLite / ONNX 모델 추론 코드로 교체
    return None


# ==========================================
# 4. 메인 제어 루프
# ==========================================
def main():
    uno = connect_arduino()
    cap = cv2.VideoCapture(0)

    # TODO: 카메라 해상도 설정 (cap.set) 및 정상 오픈 여부(cap.isOpened) 확인

    last_sent_time = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            # TODO: frame 배열 슬라이싱으로 화면 중앙 관심 영역(ROI) 잘라내기
            roi = frame

            # 판별 함수 호출
            cmd = classify_cargo(roi)
            now = time.time()

            # TODO: cmd가 '1' 또는 '2'이고 쿨다운 시간이 지났는지 확인
            # TODO: 조건 충족 시 uno.write()로 바이트 전송 및 last_sent_time 갱신

            # TODO: (선택) uno.in_waiting으로 아두이노의 응답(ACK) 읽어서 출력

            time.sleep(0.03)

    except KeyboardInterrupt:
        print("프로그램을 종료합니다.")
    finally:
        # TODO: 카메라(cap.release)와 시리얼 포트(uno.close) 안전하게 닫기
        pass


if __name__ == '__main__':
    main()