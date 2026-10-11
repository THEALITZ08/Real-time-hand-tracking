import cv2
import mediapipe as mp
import serial
import time

arduino = serial.Serial("COM3", 115200)
time.sleep(2)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)


def detect_fingers(hand_landmarks):

    finger_states = [0, 0, 0, 0, 0]

    tips = [4, 8, 12, 16, 20]

    if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0]-1].x:
        finger_states[0] = 1


    for i in range(1,5):
        if hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[tips[i]-2].y:
            finger_states[i] = 1

    return finger_states


while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame,1)

    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:

        for hand_landmarks in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            finger_state = detect_fingers(hand_landmarks)

            finger_count = sum(finger_state)

            
            cv2.putText(
                frame,
                f"Finger : {finger_count}",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2
            )

            
            arduino.write(("".join(map(str, finger_state)) + "\n").encode())

            print(finger_count)

    cv2.imshow("Hand Tracking",frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()
