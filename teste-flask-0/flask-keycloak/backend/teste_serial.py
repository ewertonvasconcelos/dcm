import serial 
import time

def sendPs2Key (data):
    strPs2ScanCodeDictionary = {
        "ArrowUp":"117",
        "ArrowDown":"114",
        "ArrowLeft":"107",
        "ArrowRight":"116",
        "1":"22",
        "2":"30",
        "3":"38",
        "4":"37",
        "5":"46",
        "6":"54",
        "7":"61",
        "8":"62",
        "9":"70",
        "0":"69" }
    #print(data)
    
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    ser.write(strPs2ScanCodeDictionary[data].encode())
    
    #print(ser.write(strPs2ScanCodeDictionary[data].encode()))
    # Serial read section
    
    #msg = ser.read(20) # read everything in the input buffer
    
    #print ("Message from arduino: ")
    #print (msg)

sendPs2Key("ArrowUp")
time.sleep(2)
sendPs2Key("ArrowUp")
time.sleep(2)
sendPs2Key("ArrowUp")
time.sleep(2)
sendPs2Key("ArrowUp")
time.sleep(2)
sendPs2Key("ArrowUp")
time.sleep(2)
sendPs2Key("ArrowUp")
time.sleep(2)
sendPs2Key("ArrowUp")
time.sleep(2)
sendPs2Key("ArrowUp")
time.sleep(2)
sendPs2Key("ArrowUp")
time.sleep(2)
sendPs2Key("ArrowUp")
time.sleep(2)
sendPs2Key("ArrowUp")
time.sleep(2)

