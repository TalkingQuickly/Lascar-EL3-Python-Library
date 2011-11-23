import time
from dataLogger import dataLoggerEL3

logger = dataLoggerEL3(0x10c4 , 0x0002, verbose=0)
logger.getConfigBlock()

#print logger.getStartOffset()

#print logger.downloadData()
#logger.getConfigBlock()
#print logger.getFlagTwo()
#print logger.getStartTime()
#print logger.getStartOffset()


#logger.startLogging()
print logger.getValidData()
#logger.stopLogging()
