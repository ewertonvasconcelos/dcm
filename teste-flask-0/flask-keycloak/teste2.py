import pyudev
import pprint
import json 


context = pyudev.Context()




def get_block_infos():

    for dev in context.list_devices(subsystem='usb-serial'):

        print('<BLOCK INFORMATION>') 
        print('Device name: %s' % dev.get('DEVPATH'))
        print('Device name: %s' % dev.get('DRIVER'))
        print('Device name: %s' % dev.get('DEVNAME'))
        print('Device type: %s' % dev.get('DEVTYPE'))
        print('Bus system: %s' % dev.get('ID_BUS'))
        print('Partition label: %s' % dev.get('ID_FS_LABEL'))
        print('FS: %s' % dev.get('ID_FS_SYSTEM_ID'))
        print('FS type: %s' % dev.get('ID_FS_TYPE'))
        print('Device usage: %s' % dev.get('ID_FS_USAGE'))
        print('Device model: %s' % dev.get('ID_MODEL'))
        print('Partition type: %s' % dev.get('ID_PART_TABLE_TYPE'))
        print('USB driver: %s' % dev.get('ID_USB_DRIVER'))
        print('Path id: %s' % dev.get('ID_PATH'))
        print(dict(dev))
        print('</BLOCK INFORMATION>')



def get_block_infos_1():

    for dev in context.list_devices(subsystem='video4linux'):

        print('<BLOCK INFORMATION>')
        print(dict(dev))
        print('Device name: %s' % dev.get('DEVPATH'))
        print('Device name: %s' % dev.get('DRIVER'))
        print('Device name: %s' % dev.get('DEVNAME'))
        print('Device type: %s' % dev.get('DEVTYPE'))
        print('Bus system: %s' % dev.get('ID_BUS'))


def get_keyboard_devs():
    context = pyudev.Context()
    
    for dev in context.list_devices(subsystem='usb-serial'):
        devStr = str(dev.get('DEVPATH')).split('/')
        print(devStr[-1],devStr[-2])


#get_block_infos()
#get_block_infos_1()
get_keyboard_devs()


#for device in context.list_devices(subsystem='usb-serial'):
#        dev = json.loads(str(dict(device)))
#        print(dev['DEVPATH'])
