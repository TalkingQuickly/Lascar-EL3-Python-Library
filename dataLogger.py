import usb.core
from datetime import datetime

class dataLoggerEL3:
    
    dev = None
    WRITEENDPOINT = 2
    READENDPOINT = 130
    ENDPOINT = 2
    TIMEOUT = 500
    verbose = 0
    configBlock = None
    doblankac=0
    connected=False
    logHandler = None
    
    
    def __init__(self,verbose=1):
        self.verbose = verbose
        self.connected=False
        #self.logHandler = logHandler
    
    
    def addLogHandler(self, handler):
        self.logHandler = handler
    
    def connect(self, vendor=0x10c4, product=0x0002):
        self.addLog("Trying to Connect" , 0 , "connect")
        self.dev = usb.core.find(idVendor=vendor, idProduct=product)
        self.addLog("Search Complete" , 0 , "connect")
        if self.dev is None:
            self.addLog("Device Not Found" , 1 , "init")
            self.connected = False
            return 0
        else:
            self.addLog("Connected to Device" , 0 , "init")
            self.getConfigBlock()
            self.connected = True 
            return 1         
        
    def addLog(self, msg, priority, caller):
        #TODO: This should raise an event which can be handled by the GUI
        if not(self.logHandler == None):
            self.logHandler(msg, priority, "dayaLogger.py:"+caller)
        if self.verbose == 1:
            print priority , ":" , msg
            
    def setConfigEtc(self):
        self.addLog("About to set config" , 0 , "setConfigEtc")
        self.dev.set_configuration()
        self.addLog("About to set Interface" , 0 , "setConfigEtc")
        self.dev.set_interface_altsetting(interface = 0, alternate_setting = 0)
        self.addLog("Interface and config set" , 0 , "setConfigEtc")
    
    def readData(self, bytes, ack=0):
        result = self.dev.read(self.READENDPOINT, bytes, 0 , self.TIMEOUT)
        if len(result)==bytes:
            self.addLog("Read: " + str(bytes) + " data: " + str(result), 0 , "readData")
        else:
            self.addLog("(Not Enough Data, only found: " + str(len(result)) +" Trying To Read: " + str(bytes) + " Read Data: " + str(result), 1 , "readData")  
        if (self.doblankac==1) & (ack==0):
            self.addLog("Writing 0 bytes ack" , 0 , "readData")
            self.writeData([] , ack=1)
        return result
    
    def writeData(self, data, ack=0):
        result = self.dev.write(self.WRITEENDPOINT , data , 0 , self.TIMEOUT)
        if len(data)==result:
            self.addLog("Correct Amount of Data Written: "+str(len(data))+" bytes. Data: " + str(data) , 0, "writeData")
        else:
            self.addLog("Sent:" , len(data) ,"to be written, actually written: " + str(result) +" bytes. Data: "+str(data) , 1 , "writeData")
        if (self.doblankac==1) & (ack==0):
            self.addLog("Reading 0 bytes ack" , 0 , "readData")
            self.readData(0, ack=1)
        return result 
    
    def controlTransfer(self, a,b):
        self.addLog("About to do control transer:  a= " + str(a) + " b= " + str(b), 0 , "controlTransfer")
        result = self.dev.ctrl_transfer(0x40, a, b, 0x00, []) 
        self.addLog("Control Transfer, a= " + str(a) + " b= " + str(b) , 0, "controlTransfer")
        return result
    
    def getConfigBlock(self, dontwrite=0):
        self.controlTransfer(0x02,0x02)
        self.writeData([0x00 , 0xff , 0xff])
        self.readData(3)
        if dontwrite==1:
            self.readData(256)
        else:
            self.configBlock = self.readData(256)   
        self.readData(1)
        self.controlTransfer(0x02,0x04)

    def setConfigBlock(self):
        if self.configBlock == None:
            self.addLog("Attempt to set config block failed, local configBlock is None" , 1 , "setConfigBlock")
            return -1
        self.controlTransfer(0x02, 0x02)
        self.writeData([0x01 , 0x00 , 0x01])
        self.writeData(self.configBlock)
        result = self.readData(1)
        self.controlTransfer(0x02, 0x04)
        self.configBlock = None
        return result

    def downloadData(self):
        compiled = []
        self.controlTransfer(0x02, 0x02)
        self.writeData([0x03, 0xFF, 0xFF])
        self.readData(3)
        for i in range(0,127):
            reading = self.readData(512)
            self.readData(1)
            compiled.append(reading)
        self.controlTransfer(0x02, 0x04)
        #print compiled
        return compiled
    
    def showConfigValues(self):
        self.getConfigBlock()
        i = 0
        for item in self.configBlock:
            print "Position:" , i , "Value:" , str(hex(item))
            i = i + 1
        
    def arrayToHex(self, values):
        #Assumes array begins with highest value
        retVal = ""
        for value in values:
            hv = str(hex(value)[2:])
            if len(hv) == 1:
                hv = "0" + str(hv)
            retVal = str(retVal) + hv
        return retVal
    
    def intToHexArray(self, value, size=0):
        #returns big endian (high byte first) 
        retval = []
        temp = str(hex(value))

        for i in range(0,len(temp)-2):
            if (i*2)+1 < len(temp):
                val = temp[(i*2)+1]
            else:
                val = ''
            retval.append(str(temp[i*2]) + val)
        
        if (size > 0) & (len(retval) < size):
            for i in range(0, size - len(retval)):
                retval.append("00")
        retval.reverse
        return retval[1:]
    
    def intToBinary(self, value, size=8):
        bstr = ''
        val2 = value
        while value > 0:
            bstr = str(value % 2) + bstr
            value = value >> 1
        if len(bstr) < size:
            for i in range(0,size-len(bstr)):
                bstr = '0' + bstr 
        
        return bstr
    
    def checkBlock(self):
        """If config block has not been loaded, this loads it."""
        if self.configBlock == None:
            self.getConfigBlock()
    
    #Begin Config Block Operations  
    
    def getDeviceType(self):
        return self.configBlock[0]
    
    def setDeviceType(self, deviceType):
        self.configBlock[0] = deviceType
        return 1
    
    def getCommand(self):
        return self.configBlock[1]
    
    def setCommand(self, command):
        self.configBlock[1] = command
        return 1
        
    def getName(self):
        #TODO: handle null termination properly
        self.checkBlock()
        name = ""
        for i in range(2, 5):
            if not (self.configBlock[i] == None):
                name = name + chr(self.configBlock[i])
        return name
    
    def setName(self, name):
        self.checkBlock()
        if len(name) > 15:
            return 0
        pos = 2
        for i in range(0, len(name)):
            #TODO: check encoding
            self.configBlock[pos] = ord(name[i])
        self.configBlock[pos+1] = 0x00 #TODO: check this, depends how it takes null termianted. 
        return 1

    def getStartTime(self):
        self.checkBlock()
        outArray = []
        outArray.append(self.configBlock[18])
        outArray.append(self.configBlock[19])
        outArray.append(self.configBlock[20])
        outArray.append(self.configBlock[21])
        outArray.append(self.configBlock[22])
        outArray.append(self.configBlock[23])
        return outArray
    
    def setStartTime(self, hours, minutes, seconds, day, month, year):
        self.checkBlock()
        self.configBlock[18] = hours
        self.configBlock[19] = minutes
        self.configBlock[20] = seconds
        self.configBlock[21] = day
        self.configBlock[22] = month
        self.configBlock[23] = year
        return 1 
    
    def getStartOffset(self):
        #TODO: currently returns array of hex values, needs to return integer
        self.checkBlock()
        return [self.configBlock[24],self.configBlock[25],self.configBlock[26],self.configBlock[27]]
    
    def setStartOffset(self, offset):
        #TODO: currently only works for an offset of 0 ie autostart
        self.checkBlock()
        if offset == 0:
            self.configBlock[24] = 0x00
            self.configBlock[25] = 0x00
            self.configBlock[26] = 0x00
            self.configBlock[27] = 0x00
    
    def getSampleRate(self):
        self.checkBlock()
        return self.arrayToHex([self.configBlock[29], self.configBlock[28]])
    
    def setSampleRate(self, sampleRate):
        self.checkBlock()
        vals = self.intToHexArray(sampleRate,2)
        self.configBlock[28] = vals[0]
        self.configBlock[29] = vals[1]
        return 1
    
    def getSampleCount(self):
        self.checkBlock()
        return self.arrayToHex([self.configBlock[31],self.configBlock[30]])
        
    def setSampleCount(self, sampleRate):
        #TODO: Check whether there is ever a need to set the sample count
        self.checkBlock()
        vals = self.intToHexArray(sampleCount,2)
        self.configBlock[30] = vals[0]
        self.configBlock[31] = vals[1]
        return 1
    
    def getRawInput(self):
        return self.arrayToHex([self.configBlock[45],self.configBlock[44]])
    
    def getFlagOne(self):
        return self.intToBinary(self.configBlock[32])
    
    def setFlagOne(self, value):
        #should be passed a value in Binary
        self.checkBlock()
        self.configBlock[32] = int(value, 2)
    
    def getFlagTwo(self):
        self.checkBlock()
        return self.intToBinary(self.configBlock[33])
    
    def getLoggingStatus(self):
        bin = self.getFlagTwo()
        return bin[7]
    
    def getDownloadStatus(self):
        bin = self.getFlagTwo()
        if bin[7] == '1':
            return '0'
        if bin[6] == '0':
            return '1'
        else:
            return '0'
        
    
    def setFlagTwo(self, value):
        #should be passed a value in Binary
        self.checkBlock()
        self.configBlock[33] = int(value, 2)
    
    def getLowBatteryThreshold(self):
        return self.arrayToHex([self.configBlock[215] , self.configBlock[214]])
    
    def setLowBatteryThreshold(self, value):
        vals = self.intToHexArray(value, 2)
        self.configBlock[215] = int(vals[0], 16)
        self.configBlock[214] = int(vals[1], 16)
    
    #End Config Block Operations
    
    #Higher Level Operations
    
    def startLogging(self):
        self.getConfigBlock()
        now = datetime.now()
        self.setStartTime(now.hour, now.minute, now.second, now.day, now.month, int(str(now.year)[2:]))
        self.setStartOffset(0)
        self.setFlagTwo('01')
        self.setConfigBlock()
        
    def stopLogging(self):
        self.getConfigBlock()
        self.setStartOffset(0)
        self.setFlagTwo('10')
        self.setConfigBlock()
    
    def getValidData(self):
        raw = self.downloadData()
        values = []
        rawhex = []
        for packet in raw:
            pos = 0
            for i in range(0, (len(packet)/2)):
                values.append(self.arrayToHex([packet[pos] , packet[pos+1]]))
                rawhex.append([packet[pos] , packet[pos+1]])
                #print pos, str(packet[pos]) , str(packet[pos+1])
                pos = pos + 2
        self.getConfigBlock()
        count = int(self.getSampleCount() , 16)
        values2 = []
        for i in range(0, count):
            val = int(values[i] , 16)
            #if val < 100:
                #print i, values[i]
            values2.append(val)
            print i, rawhex[i], self.arrayToHex([rawhex[i][0] , rawhex[i][1]])
        return values2
    #End Higher Level Operations
