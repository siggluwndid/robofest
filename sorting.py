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


def classify_cargo(roi):
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100, 120, 70])
    upper_blue = np.array([130, 255, 255])
    mask_normal = cv2.inRange(hsv, lower_blue, upper_blue)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask_hazard = cv2.bitwise_or(
        cv2.inRange(hsv, lower_red1, upper_red1),
        cv2.inRange(hsv, lower_red2, upper_red2)
    )

    if cv2.countNonZero(mask_hazard) > 2000:
        return '2'
    elif cv2.countNonZero(mask_normal) > 2000:
        return '1'
    return None


def main():
    uno = connect_arduino()
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("웹캠을 열 수 없습니다.")
        if uno is not None and uno.is_open:
            uno.close()
        return

    last_sent_time = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            h, w = frame.shape[:2]
            roi = frame[h // 4 : 3 * h // 4, w // 4 : 3 * w // 4]

            cmd = classify_cargo(roi)
            now = time.time()

            if cmd in ('1', '2') and (now - last_sent_time) >= COOLDOWN_SEC:
                if uno is not None:
                    uno.write(cmd.encode('utf-8'))
                print(f"전송 완료: {cmd}")
                last_sent_time = now

            if uno is not None and uno.in_waiting > 0:
                ack = uno.readline().decode('utf-8', errors='ignore').strip()
                if ack:
                    print(f"우노 응답: {ack}")

            time.sleep(0.03)

    except KeyboardInterrupt:
        print("프로그램을 종료합니다.")
    finally:
        cap.release()
        if uno is not None and uno.is_open:
            uno.close()


if __name__ == '__main__':
    main()