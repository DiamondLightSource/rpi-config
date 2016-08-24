import com.hopding.jrpicam as RPiCam
import time

class Camera:
    def __init__(self):
        self.dirStub = "/home/pi/"
        self.cam = RPiCam.RPiCamera()