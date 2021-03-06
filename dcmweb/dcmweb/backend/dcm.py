import serial
import time 
from collections import defaultdict
import pyudev
import subprocess
from ..backend.models import Server, db
import netplan
import socket


def SendUsbKeyboard(key,dev):
    ser = serial.Serial('/dev/{}'.format(dev), 9600)
    print(key)

    keyCodeDictionary = {
        "PowerButtonPress":"1200",
        "ResetButtonPress":"1201",
        "ArrowUp":"1000",
        "ArrowDown":"1001",
        "ArrowLeft":"1002",
        "ArrowRight":"1003",
        "Delete":"1004",
        "Enter":"1005",
        "Escape":"1006" ,
        "Backspace":"1007",
        "Tab":"1008",
        "PrintScreen":"1009",
        "Home":"1010",
        "End":"1011",
        "Insert":"1012",
        "PageUp":"1013",
        "PageDown":"1014",
        "Shift":"1015",
        "Alt":"1016",
        "Control":"1017",
        "OS":"1018",
        "Meta":"1018",
        "ctrl+alt+del":"1019",
        "NumLock":"1020",
        "alt+f4":"1022",
        "CapsLock":"",
        "F1":"1101",
        "F2":"1102",
        "F3":"1103",
        "F4":"1104",
        "F5":"1105",
        "F6":"1106",
        "F7":"1107",
        "F8":"1108",
        "F9":"1109",
        "F10":"1110",
        "F11":"1111",
        "F12":"1112",
        "Dead":"",
        "|":"",
        "^":"",
        "~":"",
        "ç":"1023",
        "Ç":"1024",
        "[":"1025",
        "{":"1026",
        "]":"1027",
        "}":"1028",
        "'":"1029",
        "\"":"1030",
        ":":"1031",
        ";":"1032"
}

    toSend = defaultdict(lambda: key, keyCodeDictionary)
    ser.write(toSend[key].encode())
        
    return 0


def ManageService(serviceName, action):
    Command = 'sudo service '+serviceName+' '+action
    ActionResult = subprocess.Popen(Command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    OK, ERR = ActionResult.communicate()

    if ERR is None:
        print("- The service {} was successfully {}ed!".format(serviceName, action))
    else:
        print("ERROR: To {} the service {}".format(action, serviceName))

    return ERR



def get_mgnt_devs():
    context = pyudev.Context()
    devsList = []
    for dev in context.list_devices(subsystem='usb-serial'):
        devStr = str(dev.get('DEVPATH')).split('/')
        devsList.append(devStr[-1]+' @ '+devStr[-2])
    
    return devsList

def get_video_devs():
    context = pyudev.Context()
    devsList = []
    for dev in context.list_devices(subsystem='video4linux'):
        devStr = str(dev.get('DEVPATH')).split('/')
        devsList.append(devStr[-1]+' @ '+devStr[-3])
    
    return devsList

def UpdateMgntDevicesLocation ():
    try:
        mgntDevsList = get_mgnt_devs()
        serversList = Server.query.all()

        for server in serversList:
            for mgntDev in mgntDevsList:
                if(mgntDev.split(" ")[-1] == server.mgnt_port.split(" ")[-1]):
                    dev = mgntDev.split(" ")[0]
                    server.mgnt_port = mgntDev
                    db.session.commit()
                    break
        
        return serversList
    except:
        return -1



def sendPs2Key (data):
    # For special characters, we sum 2k to the real value to differenciate on the arduino
    strPs2ScanCodeDictionary = {
        "ArrowUp":"2117",
        "ArrowDown":"2114",
        "ArrowLeft":"2107",
        "ArrowRight":"2116",
        "Delete":"2113",
        "Enter":"90",
        "Escape":"118",
        "Backspace":"102",
        "F1":"5",
        "F2":"6",
        "F3":"4",
        "F4":"12",
        "F5":"3",
        "F6":"11",
        "F7":"131",
        "F8":"10",
        "F9":"1",
        "F10":"9",
        "F11":"120",
        "F12":"7",
#         "SCROLL_LOCK":"126",
#         "ACCENT":"14",
#         "SEVEN":"61",
#         "EIGHT":"62",
#         "NINE":"70",
#         "ZERO":"69",
#         "MINUS":"78",
#         "EQUAL":"85",
        "Tab":"13",
        "Q":"21",
        "W":"29",
        "E":"36",
        "R":"45",
        "T":"44",
        "Y":"53",
        "U":"60",
        "I":"67",
        "O":"68",
        "P":"77",
        "q":"21",
        "w":"29",
        "e":"36",
        "r":"45",
        "t":"44",
        "y":"53",
        "u":"60",
        "i":"67",
        "o":"68",
        "p":"77",
        "[":"84",
        "]":"91",
        "\\":"93",
        "CapsLock":"88",
        "A":"28",
        "S":"27",
        "D":"35",
        "F":"43",
        "G":"52",
        "H":"51",
        "J":"59",
        "K":"66",
        "L":"75",
        "a":"28",
        "s":"27",
        "d":"35",
        "f":"43",
        "g":"52",
        "h":"51",
        "j":"59",
        "k":"66",
        "l":"75",
        ";":"76",
        "'":"82",
        "Shift":"18",
        "Z":"26",
        "X":"34",
        "C":"33",
        "V":"42",
        "B":"50",
        "N":"49",
        "M":"58",
        "z":"26",
        "x":"34",
        "c":"33",
        "v":"42",
        "b":"50",
        "n":"49",
        "m":"58",
        ",":"65",
        ".":"73",
        "/":"74",
        "Shift":"89",
        "Control":"20",
        "Alt":"17",
        " ":"41",
        "NumLock":"119",
        "*":"124",
        "-":"123",
        "+":"121",
         ",":"113",
#---
        "1":"22",
        "2":"30",
        "3":"38",
        "4":"37",
        "5":"46",
        "6":"54",
        "7":"61",
        "8":"62",
        "9":"70",
        "0":"69",
        "OS":"2031",
        # "RIGHT_ALT":""17",
        # "RIGHT_WIN":""39",
        # "MENUS":""47",
        # "RIGHT_CONTROL":""20",
         "insert":"2112",
         "home":"2108",
        # "PAGE_UP":""125",
        # "DELETE":""113",
        # "END":""105",
        # "PAGE_DOWN":""122",
        # "UP_ARROW":""117",
        # "LEFT_ARROW":""107",
        # "DOWN_ARROW":""114",
        # "RIGHT_ARROW":""116",
        # "DIVIDE":""74",
        # "NUMPAD_ENTER":""90",
        # "NEXT_TRACK":""77",
        # "PREVIOUS_TRACK":""21",
        # "STOP":""59",
        # "PLAY_PAUSE":""52",
        # "MUTE":""35",
        # "VOLUME_UP":""50",
        # "VOLUME_DOWN":""33",
        # "MEDIA_SELECT":""80",
        # "EMAIL":""72",
        # "CALCULATOR":""43",
        # "MY_COMPUTER":""64",
        # "WWW_SEARCH":""16",
        # "WWW_HOME":""58",
        # "WWW_BACK":""56",
        # "WWW_FORWARD":""48",
        # "WWW_STOP":""40",
        # "WWW_REFRESH":""32",
        # "WWW_FAVORITES":""24",
        # "POWER":""94",
        # "SLEEP":""95",
        # "WAKE":""99",
        "=":"85"
        }

    print(strPs2ScanCodeDictionary[data])
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    ser.write(strPs2ScanCodeDictionary[data].encode())


def getPowerStateFromMgnt(dev):
    ser = serial.Serial('/dev/{}'.format(dev), 9600)
    requestId = '1202'
    ser.write(requestId.encode())
    state = ser.read().decode()
    
    print('State:',state)

    if(state=='0'):
         serverState='ON'
    else:
         serverState='OFF'
    #serverState='ON'
    
    return serverState


def updateServerPowerState(server_id,state):
    try:
        server = Server.query.filter_by(id=server_id).first()
        if server.status != state :
            server.status = state
            db.session.commit()
    except:
            return -1


def ConfigureNetplan(ipnetmask,gateway,dns):
    if (ipnetmask == ""):
        Command ='''sudo echo \"# This file describes the network interfaces available on your system
# For more information, see netplan(5).
network:
    version: 2
    renderer: networkd
    ethernets:
        ens32:
            dhcp4: yes\" > /etc/netplan/01-netcfg.yaml '''.format(ipnetmask,gateway,','.join(dns))
    else:
        Command ='''sudo echo \"# This file describes the network interfaces available on your system
# For more information, see netplan(5).
network:
    version: 2
    renderer: networkd
    ethernets:
        ens32:
            dhcp4: no
            addresses:
                - {}
            gateway4: {}
            nameservers:
                addresses: [{}] \" > /etc/netplan/01-netcfg.yaml '''.format(ipnetmask,gateway,','.join(dns))

    print(socket.gethostbyname(socket.gethostname()))
    # print(Command)

    # ActionResult = subprocess.Popen(Command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # OK, ERR = ActionResult.communicate()

    # if ERR is None:
    #     print("- Netplan file configured")
    # else:
    #     print("- Fail to create Netplan file")
    #     return ERR

    # Command ='sudo netplan apply'

    # ActionResult = subprocess.Popen(Command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # OK, ERR = ActionResult.communicate()
    # if ERR is None:
    #     print("- Netplan configuration applied")
    # else:
    #     print("- Fail to apply Netplan configuration")

    # return ERR

