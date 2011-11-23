from dataHandler import tcDataHandler
import datetime

class tcDataHandlerEL3(tcDataHandler):
    def genData(self, values, startTime, sampleRate):
        #Generates list of lines ready for writeFile, pre ramp extraction
        #start Time is array: [year, month, day, hour, minute, second]
        startTime[5] = int('20' + str(startTime[5]))
        time = datetime.datetime(startTime[5],startTime[4],startTime[3],startTime[0],startTime[1],startTime[2])
        inc = datetime.timedelta(0,sampleRate)
        outArray = []
        for point in values:
            outArray.append(str(time) + "," + str(point) + '\n')
            time = time + inc
        return outArray
    
    def 
    
    def storeData(self, values, startDate, sampleRate, fileName, filePath=''):
        data = self.genData(values, startDate, sampleRate)
        self.writeFile(data, fileName, filePath)
    
    #Start High Level Functions# 
    
    def dataBackup(self, values, startDate, sampleRate):
        #Auto generates filename to store data backup when a download takes place
        data = self.genData(values, startDate, sampleRate)
        self.writeFile(data, self.dateStamp(datetime.datetime.now() , time=True)+'.csv')
    
    #End High Level Functions#

if __name__ == '__main__':
    print "Testing dataHandlerEL3.py Class"
    testClass = tcDataHandlerEL3()
    data = [0,1,2,3,4,5,6,7,8]
    dt = [2010,02,16,16,8,3]
    sr = 1
    print testClass.genData( data, dt , sr)
    testClass.dataBackup(data, dt , sr)
    testClass.storeData(data, dt , sr , "Test File.csv")
