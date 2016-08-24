import com.hopding.jrpicam as RPiCam
from datetime import date

class Camera:
    def __init__(self):
        self.date = date.today()
        self.dirStub = "/home/pi/gda_data_non_live"
        self.fileCount = 0
        dirCheck()
        if fileCount == -1:
            fileFind()
        self.cam = RPiCam.RPiCamera(self.fullDir)
        
        
                
    def dirCheck(self):
        self.fullDir = dirStub +"/"+ str(self.date.year) +"/"+ str(self.date.month) +"/"+ str(self.date.day)
        if not os.path.exists(self.fullDir):
            os.makedirs(self.fullDir)
        else:
            self.fileCount = -1
            
    def fileFind(self):
        ##check for files and find next clear Value
        