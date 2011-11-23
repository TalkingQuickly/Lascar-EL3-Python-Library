def arrayToHex(self, values):
    #Assumes array begins with highest value
    retVal = ""
    for value in values:
        retVal = str(retVal) + str(hex(value)[2:])
    return retVal

print arrayToHex(500)
