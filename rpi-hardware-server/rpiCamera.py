import com.hopding.jrpicam as RPiCam
from datetime import date
import os
from os import path

class Camera:
    def __init__(self):
        self.dirStub = "/home/pi/gda_data_non_live"
        self.defaultFileName = "000001.jpg"
        self.fileName = self.defaultFileName
        self.fileCount = 0
        self.cam = RPiCam.RPiCamera()
        self.cam.setTimeout(0)
        
    def parse(self, num, instr, command, pathString, duration):
        print command
        print pathString
        if (command == "start"):
            self.scanStart(pathString.lower())
            return 0
        elif (command == "capture"):
            file = self.take()
            return ("-1,True,"+file+",Image Captured//")
        else:
            return 5 
                
    def dirCheck(self, path):
        self.fullDir = path
        if not os.path.exists(self.fullDir):
            os.makedirs(self.fullDir)
            self.fileFind()
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
        self.fileName = self.defaultFileName
        self.dirCheck(path)
        self.cam.setSaveDir(path)
    
    def take(self):
        print self.fileName
        self.cam.takeStill(self.fileName, 2592, 1944)
        takenFile = self.fullDir+"/"+self.fileName
        self.nextFile()
        return takenFile
    