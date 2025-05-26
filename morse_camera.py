import cv2
import time
from morse_log import log

class Camera():
    def __init__(self):
        self.width = 640
        self.height = 480
        self.fps = 15  # Target FPS cap
        self.frame_delay = 1.0 / self.fps  # Delay per frame
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FPS, 15)


        # Set frame width and height if needed
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)

        print(f"Camera warming up ... Target FPS: {self.fps}")
        time.sleep(1)
        self.ret, self.frame = self.cap.read()
        self.last_frame_time = time.time()

    def get_frame(self):
        now = time.time()
        elapsed = now - self.last_frame_time

        if elapsed < self.frame_delay:
            time.sleep(self.frame_delay - elapsed)

        self.last_frame_time = time.time()
        success, image = self.cap.read()

        if not success:
            return b''  # Return empty bytes if capture fails

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        print("Camera disabled and all output windows closed")
        log("Camera disabled and all output windows closed")
