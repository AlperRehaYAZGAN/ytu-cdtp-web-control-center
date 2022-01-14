import socket
import struct
import cv2
from multiprocessing import Queue
import math
import numpy as np


class Camera():
    MAX_DGRAM = 2**16
    MAX_IMAGE_DGRAM = MAX_DGRAM - 64  # extract 64 bytes in case UDP frame overflown

    def __init__(self, port=12346, addr="192.168.1.30", bind=False):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = port
        self.addr = addr

        if bind:
            while True:
                try:
                    self.sock.bind((self.addr, self.port))
                    print("binded successfully!")
                    self.data = b''
                    self.q = Queue(self.MAX_DGRAM)
                    break
                except:
                    pass

    def gstreamer_pipeline(
            self,
            capture_width=960,
            capture_height=540,
            display_width=960,
            display_height=540,
            framerate=60,
            flip_method=2,
    ):
        return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
        )

    def udp_frame(self, img):
        percent = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        encoded = cv2.imencode('.jpg', img, percent)[1]
        converted = encoded.tobytes()
        size = len(converted)
        count = math.ceil(size/(self.MAX_IMAGE_DGRAM))
        array_pos_start = 0
        while count:
            array_pos_end = array_pos_start + self.MAX_IMAGE_DGRAM
            self.sock.sendto(struct.pack(
                "B", count) + converted[array_pos_start:array_pos_end], (self.addr, self.port))
            array_pos_start = array_pos_end
            count -= 1

    def SendCamera(self):
        cap = cv2.VideoCapture(self.gstreamer_pipeline(
            flip_method=0), cv2.CAP_GSTREAMER)
        while (cap.isOpened()):
            try:
                _, frame = cap.read()
                self.udp_frame(frame)
            except:
                pass

        cap.release()
        cv2.destroyAllWindows()
        self.sock.close()

    def ReceiveCamera(self):
        while True:
            frame, addr = self.sock.recvfrom(self.MAX_DGRAM)
            if struct.unpack("B", frame[0:1])[0] > 1:
                self.q.put(frame[1:])
                # self.data += frame[1:]
            else:
                self.q.put(frame[1:])
                # self.data += frame[1:]
                while self.q.qsize() > 0:
                    self.data += self.q.get()

                decoded = cv2.imdecode(np.frombuffer(
                    self.data, dtype=np.uint8), 1)
                resize = cv2.resize(decoded, (640, 480))
                cv2.imshow('frame', resize)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                self.data = b''
        # cap.release()
        cv2.destroyAllWindows()
        self.sock.close()


if __name__ == "__main__":
    cs = Camera()
    cs.SendCamera()