import os
from datetime import datetime
import sys

class tcDataHandler:
    
    dataPath = None
    logPath = None
    logFileName = None
    loggingLevel = 0 # Denotes the lowest level of message to log, 0 is verbose
    
    def __init__(self, dataPath='', logPath=''):
        if dataPath == '':
            dataPath = os.getcwd() + '/data/'
        if logPath == '':
            logPath = os.getcwd() + '/logs/'
        self.dataPath = dataPath
        self.logPath = logPath
        self.checkExists(self.dataPath)
        self.checkExists(self.logPath)
        now = datetime.now()
        self.logFileName = self.dateStamp(now) +'.log'
        self.loadConfig()
    
    def self.loadConfig():
        #loads values from configuration files, defined in subclasses.
        pass
    
    def dateStamp(self,date, time=False, now=False):
        if now == True:
            date = datetime.now()
        dateString = str(date.day) +"-"+ str(date.month) + "-"+str(date.year)
        timeString = ''
        if time == True:
            timeString = '_' + str(date.hour) +"-"+ str(date.minute) +"-"+ str(date.second)
        return dateString + timeString
    
    def checkExists(self, path, create=True):
        if not os.path.exists(path):
            os.makedirs(path)
    
    def logError(self, message, priority, source, timeStamp):
        if priority >= self.loggingLevel:
            self.appendToLog([timeStamp , priority, message, source] , self.logFileName)
    
    def writeFile(self, data, fileName, path=''):
        #Data should be in the form of a list of strings
        if path == '':
            path = self.dataPath
        else:
            checkExists(path)
        fullPath = path + fileName
        try:
            f = open(fullPath, "w")
            try:
                f.writelines(data)
            finally:
                f.close()
        except IOError:
            print sys.exc_info()[0]
    
    def appendToLog(self, line, fileName, path=''):
        #line should be a one dimensional array
        #0 - Date and Time
        #1 - Priority
        #2 - Message
        #3 - Source 
        #fileName should be the name of log file
        fullLine = str(line[0])
        fullLine += "| Priority: " + str(line[1])
        fullLine += "| Message: " + line[2]
        fullLine += "| Source: " + line[3]
        
        if path == '':
            path = self.logPath
        fullPath = path + fileName
        
        try:
            logfile = open(fullPath, "a")
            try:
                logfile.write(fullLine + '\n')
            finally:
                logfile.close()    
        except IOError:
            print sys.exc_info()[0]
        
if __name__ == '__main__':
    print "Testing Module dataHandler"
    testClass = tcDataHandler()
    print "Data Path:" , testClass.dataPath
    print "Log Path:" , testClass.logPath
    print "Data File Name:" , testClass.logFileName
    print "Writing Test Message to Log File"
    testClass.logError("Test Message" , 0, "TR" ,datetime.now())
    print "Test Line Written"
    print "Writing 3 test lines to time stamped Data File"
    testClass.writeFile(["line1\n" , "line2\n" , "line3\n"] , str(datetime.now()))
    print "Written lines to file"
