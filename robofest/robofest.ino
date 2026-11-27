#include <Servo.h>

Servo servo;

const int servo_pin = 3;
const int redred = 5;
const int ylyl = 6;
const int grgr = 9;

void setup() {
  pinMode(redred, OUTPUT);
  pinMode(ylyl, OUTPUT);
  pinMode(grgr, OUTPUT);

  servo.attach(servo_pin);
  servo.write(0);
  digitalWrite(ylyl, HIGH);

  Serial.begin(9600);
}

void loop() {

  if (Serial.available() > 0) {
    char cmd = Serial.read(); //라즈베리파이에서 시리얼 코드를 받아옵니다.

    if (cmd == '1') {
      servo.write(30);  // 라즈베리파이에서 받아온 시리얼 코드 정보를 바탕으로 서보모터를 움직여 화물이 정상적으로 움직이게 합니다.
      digitalWrite(redred, LOW);
      digitalWrite(ylyl, LOW); 
      digitalWrite(grgr, HIGH);
      delay(1500);
    } else if (cmd == '2') {
      servo.write(90);  //만약 위험물 일시에 서보모터 각도를 완전 아래로 꺾어 화물이 위험물 관리토으로 떨어지게 합니다.
      digitalWrite(grgr, LOW);
      digitalWrite(ylyl, LOW);
      digitalWrite(redred, HIGH);
      delay(1500);
    }

    servo.write(0);
    digitalWrite(redred, LOW);
    digitalWrite(grgr, LOW);
    digitalWrite(ylyl, HIGH);

    while (Serial.available() > 0) {
      Serial.read();
    } //잔여 찌꺼기 데이터르 지우고 재실행합니다.
  }
}