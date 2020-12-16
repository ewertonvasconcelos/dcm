import serial

def sendPs2Key (data):
    # For special characters, we sum 2k to the real value to differenciate on the arduino
    strPs2ScanCodeDictionary = {
        "ArrowUp":"2117",
        "ArrowDown":"2114",
        "ArrowLeft":"2107",
        "ArrowRight":"2116",
        "delete":"2113",
        "Enter":"90",
        "Escape":"118",
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

    print(strPs2ScanCodeDictionary[data])
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    ser.write(strPs2ScanCodeDictionary[data].encode())

