from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
from morse_converter import convertMorseToText
from collections import deque
import numpy as np
from morse_log import log

class Detectmorse():
    def __init__(self):
        self.flag = 0
        self.openEye = 0
        self.current_morse_seq = []
        self.finalString = []
        self.pts = deque(maxlen=512)
        self.thresh = 0.26  # EAR threshold (adjusted slightly)
        self.detect = dlib.get_frontal_face_detector()
        self.predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    def eye_aspect_ratio(self, eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def calculate(self, frame):
        decoded = cv2.imdecode(np.frombuffer(frame, np.uint8), -1)
        frame = imutils.resize(decoded, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        subjects = self.detect(gray, 0)
        for subject in subjects:
            shape = self.predict(gray, subject)
            shape = face_utils.shape_to_np(shape)

            leftEye = shape[self.lStart:self.lEnd]
            rightEye = shape[self.rStart:self.rEnd]

            leftEAR = self.eye_aspect_ratio(leftEye)
            rightEAR = self.eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)

            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            if ear < self.thresh:  # eyes closed
                self.flag += 1
                self.openEye = 0
                self.pts.appendleft(self.flag)
            else:  # eyes open
                if self.flag != 0:
                    blink_length = self.flag
                    self._interpret_blink(blink_length)
                self.flag = 0
                self.openEye += 1
                self.pts.appendleft(self.flag)

        # If open eyes for certain frames, decode Morse
        if self.openEye > 25 and self.current_morse_seq:
            morse_code = ''.join(self.current_morse_seq)
            decoded_char = convertMorseToText(morse_code)
            if decoded_char:
                self.finalString.append(decoded_char)
                log(f"Decoded character: {decoded_char}")
            else:
                log(f"Failed to decode: {morse_code}")
            self.current_morse_seq = []

        # Draw final decoded text
        final_text = ''.join(self.finalString)
        morse_text = ''.join(self.current_morse_seq)

        cv2.putText(frame, "Morse: " + morse_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.putText(frame, "Decoded: " + final_text, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (52, 152, 219), 2)

        ret, png = cv2.imencode('.png', frame)
        return png, self.current_morse_seq

    def _interpret_blink(self, frames_closed):
        if 4 <= frames_closed < 8:
            self.current_morse_seq.append('.')
            log(f"Dot detected ({frames_closed} frames)")
            print(f"Dot detected ({frames_closed} frames)")
        elif 8 <= frames_closed < 15:
            self.current_morse_seq.append('-')
            log(f"Dash detected ({frames_closed} frames)")
            print(f"Dash detected ({frames_closed} frames)")
        elif frames_closed >= 15:
            if self.current_morse_seq:
                removed = self.current_morse_seq.pop()
                log(f"Long blink detected, removed last Morse character: {removed}")
                print(f"Long blink detected, removed last Morse character: {removed}")

    @property
    def final(self):
        return ''.join(self.finalString)
