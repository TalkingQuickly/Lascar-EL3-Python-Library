import usb.core
import time

LOGGER_VENDOR = 0x10c4
LOGGER_PRODUCT = 0x0002

print "trying to connect to usb Device"
dev = usb.core.find(idVendor=LOGGER_VENDOR, idProduct=LOGGER_PRODUCT)

print "CT35 (0x02 0x02):" , dev.ctrl_transfer(0x40, 0x02, 0x02, 0x00, []) 
print "Request Recorded Data (03 ff ff)" , dev.write(2, [0x03 , 0xff , 0xff] , 0 , 100)
print "Response from Device:" , dev.read(2 , 3 , 0 , 100)
print "Entering Loop"
for i in range(1,100):
    print "Reading Data Packet:" , i ,  "output:" , dev.read(2 , 255 , 0 , 100)
    #print "Writing Acknowledgement (0 bytes)" , dev.write(2, [] , 0 , 100)
    
print "Done Getting Data"
