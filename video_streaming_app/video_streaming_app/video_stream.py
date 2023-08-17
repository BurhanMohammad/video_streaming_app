import cv2
import threading

class VideoStream(threading.Thread):
    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.frame = None
        self.stopped = False

    def run(self):
        cap = cv2.VideoCapture(self.video_path)

        while not self.stopped:
            ret, frame = cap.read()
            if not ret:
                self.stop()
                break
            self.frame = frame

        cap.release()

    def stop(self):
        self.stopped = True

    def generate_frames(self):
        while not self.stopped:
            if self.frame is not None:
                _, buffer = cv2.imencode('.jpg', self.frame)
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

