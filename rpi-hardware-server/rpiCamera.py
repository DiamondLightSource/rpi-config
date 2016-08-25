import com.hopding.jrpicam as RPiCam
from datetime import date
import os
import path

class Camera:
    def __init__(self):
        self.date = date.today()
        self.dirStub = "/home/pi/gda_data_non_live"
        self.defaultFileName = "000001.jpg"
        self.fileName = self.defaultFileName
        self.fileCount = 0
        self.dirCheck()
        self.cam = RPiCam.RPiCamera()
        self.cam.setToDefaults()
        self.cam.setTimeout(0)
        
    def parse(self, num, instr, pathString, pinState, duration):
        if (instr == "START"):
            self.scanStart(pathString)
        elif (instr == "CAPTURE"):
            self.take()
                        
                
    def dirCheck(self, path):
        self.fullDir = dirStub +"/"+ str(self.date.year) +"/"+path
        if not os.path.exists(self.fullDir):
            os.makedirs(self.fullDir)
        else:
            self.findFile()
            
    def fileFind(self):
        noFile = False
        while (noFile == False):
            if os.path.isfile(self.fullDir+"/"+self.fileName):
                self.nextFile() 
            else:
                noFile = True
                self.fileName = self.defaultFileName
            
    def nextFile(self):
        fileInt = int(self.fileName[:6])
        fileInt += 1
        self.fileName = str(fileInt)+".jpg"
        while len(self.fileName < 10):
            self.fileName = "0"+self.fileName
    
    def scanStart(self, path):
        self.dirCheck(path)
        self.cam.setSaveDir(path)
    
    def take(self):
        self.cam.takeStill(self.fileName)
        takenFile = self.fullDir+"/"+self.fileName
        self.nextFile()
        return takenFile
    