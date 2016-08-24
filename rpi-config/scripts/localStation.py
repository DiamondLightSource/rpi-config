import sys    
import os
import time
from gda.factory import Finder
from gda.configuration.properties import LocalProperties
from gdascripts.messages import handle_messages
from gda.jython import InterfaceProvider
from gda.device.scannable import ScannableBase
import rpiComms
import rpiScannable
import arduinoScannable
from rpiComms import initaliseCommunicator
import arduinoMotor

        
def isLive():
    mode = LocalProperties.get("gda.mode")
    return mode =="live"

try:
    from gda.device import Scannable
    from gda.jython.commands.GeneralCommands import ls_names, vararg_alias
    
    def ls_scannables():
        ls_names(Scannable)
    
    alias("ls_scannables")


    from epics_scripts.pv_scannable_utils import createPVScannable, caput, caget
    alias("createPVScannable")
    alias("caput")
    alias("caget")
    
    from gda.scan.RepeatScan import create_repscan, repscan
    vararg_alias("repscan")

    #setup tools to create metadata in Nexus files
    from gdascripts.metadata.metadata_commands import setTitle, meta_add, meta_ll, meta_ls, meta_rm
    alias("setTitle")
    alias("meta_add")
    alias("meta_ll")
    alias("meta_ls")
    alias("meta_rm")
    from gda.data.scan.datawriter import NexusDataWriter
    LocalProperties.set(NexusDataWriter.GDA_NEXUS_METADATAPROVIDER_NAME,"metashop")
    
    #create time scannables
    from gdascripts.pd.time_pds import waittimeClass2, showtimeClass, showincrementaltimeClass, actualTimeClass
    waittime=waittimeClass2('waittime')
    showtime=showtimeClass('showtime')
    inctime=showincrementaltimeClass('inctime')
    actualTime=actualTimeClass("actualTime")
    
    #RPiScannables     
    rpiComms.initaliseCommunicator("p45-pi-01.diamond.ac.uk")
    
    led1=rpiScannable.rpiScannable("LED1", 29, "output")
    button1=rpiScannable.rpiScannable("BUTTON1", 28, "input")
    
    UNOpwm1 = arduinoScannable.arduinoScannable("UNOpwm1", 3, "arduino-01","p")
    UNObutton1 = arduinoScannable.arduinoScannable("UNObutton1", 12, "arduino-01", "i")
    UNOanalog1 = arduinoScannable.arduinoScannable("UNOanalog1", 2, "arduino-01", "a")
    
    UNOmotor1a = arduinoScannable.arduinoScannable("UNOmotor1a", 8, "arduino-01", "o")
    UNOmotor1b = arduinoScannable.arduinoScannable("UNOmotor1b", 9, "arduino-01", "o")
    UNOmotor1c = arduinoScannable.arduinoScannable("UNOmotor1c", 10, "arduino-01", "o")
    UNOmotor1d = arduinoScannable.arduinoScannable("UNOmotor1d", 11, "arduino-01", "o")
    UNOmotor1 = arduinoMotor.arduinoMotor("UNOmotor1", UNOmotor1a, UNOmotor1b, UNOmotor1c, UNOmotor1d)

    #run user editable startup script 
    if isLive():
        run("localStationUser.py")

except:
    exceptionType, exception, traceback = sys.exc_info()
    handle_messages.log(None, "Error in localStation", exceptionType, exception, traceback, False)

