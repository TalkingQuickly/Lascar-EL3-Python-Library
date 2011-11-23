import usb.core

print "trying to connect to usb Device"
dev = usb.core.find(idVendor=0x10c4, idProduct=0x0002)
if dev is None:
    raise ValueError('Our device is not connected')
else :
    print "Device Connected OK"

for cfg in dev:
    print "Configuration: " , str(cfg.bConfigurationValue) + '\n'
    for intf in cfg:
        print "intf.InterfaceNumber:" , str(intf.bInterfaceNumber) , "intf.AlternateSetting:" , str(intf.bAlternateSetting)
        for ep in intf:
            print "Endpoint Address:" , str(ep.bEndpointAddress) 
            
#print "Trying to Set Config (Using First Found)"
#dev.set_configuration()
#print "Config Set OK"
#print "Trying to select interface 0 and alternate_setting to 0"
#dev.set_interface_altsetting(interface = 0, alternate_setting = 0)
#print "Config Set OK"


print "CT15 (0x02 0x02):" , dev.ctrl_transfer(0x40, 0x02, 0x02, 0x00, []) 
print "W16 (00 ff ff)" , dev.write(2, [0x00 , 0xff , 0xff] , 0 , 100)
print "R16:", dev.read(130 , 3 , 0 ,100)
#print "W17 ()" , dev.write(2, [] , 0 , 100)
print "R17:", dev.read(130 , 256 , 0 ,100)
#print "W18 ()" , dev.write(2, [] , 0 , 100)
print "R18:", dev.read(130 , 1 , 0 ,100)
print "CT19 (0x02 0x04):" , dev.ctrl_transfer(0x40, 0x02, 0x04, 0x00, []) 
print "CT20 (0x02 0x04):" , dev.ctrl_transfer(0x40, 0x02, 0x02, 0x00, [])
print "W21 (01 00 01)" , dev.write(2, [0x01 , 0x00 , 0x01] , 0 , 100)
print "R21:", dev.read(130 , 3 , 0 ,100)
print "W22 (Setup data)" , dev.write(2, [0x06 ,0x00 ,0x45 ,0x61 ,0x73 ,0x79 ,0x4c ,0x6f ,0x67 ,0x20 ,0x55 ,0x53 ,0x42 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x11 ,0x32 ,0x25 ,0x10 ,0x0b ,0x09 ,0x00 ,0x00 ,0x00 ,0x00 ,0x01 ,0x00 ,0x3b ,0x00 ,0x00 ,0x03 ,0xf4 ,0xc8 ,0x7e ,0xf9 ,0x1d ,0x38 ,0xf5 ,0xbf ,0xf3 ,0xba ,0x08 ,0x00 ,0x00 ,0x00 ,0x76 ,0x30 ,0x2e ,0x33 ,0xad ,0x3d ,0x00 ,0x00 ,0x58 ,0x28 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x56 ,0x6f ,0x6c ,0x74 ,0x73 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x30 ,0x2e ,0x30 ,0x30 ,0x00 ,0x00 ,0x00 ,0x00 ,0x30 ,0x2e ,0x30 ,0x30 ,0x00 ,0x00 ,0x00 ,0x00 ,0x33 ,0x30 ,0x2e ,0x30 ,0x30 ,0x00 ,0x00 ,0x00 ,0x33 ,0x30 ,0x2e ,0x30 ,0x30 ,0x00 ,0x00 ,0x00 ,0x67 ,0xa3 ,0x4e ,0x41 ,0x32 ,0x35 ,0x2e ,0x30 ,0x30 ,0x00 ,0x00 ,0x00 ,0x35 ,0x2e ,0x30 ,0x30 ,0x00 ,0x00 ,0x00 ,0x00 ,0x30 ,0x2e ,0x30 ,0x30 ,0x20 ,0x2d ,0x20 ,0x33 ,0x30 ,0x2e ,0x30 ,0x30 ,0x00 ,0x00 ,0x56 ,0x6f ,0x6c ,0x74 ,0x73 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x56 ,0x6f ,0x6c ,0x74 ,0x73 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x30 ,0x2e ,0x30 ,0x30 ,0x00 ,0x00 ,0x00 ,0x00 ,0x30 ,0x2e ,0x30 ,0x30 ,0x00 ,0x00 ,0x00 ,0x00 ,0x33 ,0x30 ,0x2e ,0x30 ,0x30 ,0x00 ,0x00 ,0x00 ,0x33 ,0x30 ,0x2e ,0x30 ,0x30 ,0x00 ,0x00 ,0x00 ,0x32 ,0x35 ,0x2e ,0x30 ,0x30 ,0x00 ,0x00 ,0x00 ,0x35 ,0x2e ,0x30 ,0x30 ,0x00 ,0x00 ,0x00 ,0x00 ,0x38 ,0x02 ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff ,0xff] ,0 , 100)
print "R22:", dev.read(130 , 256 , 0 ,100)
#print "W23 ()" , dev.write(2, [] , 0 , 100)
print "CT24 (0x02 0x04):" , dev.ctrl_transfer(0x40, 0x02, 0x04, 0x00, []) 