import psutil
import subprocess

def StopNotUsedStreamers():
    actives = []
    connList = psutil.net_connections()

    #Add services active to the list:0

    for conn in connList: 
        port = conn.laddr.port
        status =  conn.status
        #print(conn)
        if(port >= 8100 and port <= 8199):
            if((port not in actives) and (status!='ESTABLISHED')):
                actives.append(port)

    #Remove used services:

    for conn in connList: 
        port = conn.laddr.port
        status =  conn.status
        #print(conn)
        if(port >= 8100 and port <= 8199):
            if((port in actives) and (status=='ESTABLISHED')):
                for i in actives:
                    actives.remove(port)

    #Stop not used streamers:
    for port in actives:
        streamerNum = str(port)[-2]
        status = ManageService('ustreamer@"'+streamerNum+'"','stop')
        time.sleep(1)

def ManageService(serviceName,action):
    Command = 'service '+serviceName+' '+action
    ActionResult = subprocess.Popen(Command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    OK, ERR = ActionResult.communicate()
    if ERR is None:
        print("OK: The service {} was successfully started!".format(serviceName))
    else:
        print("ERROR: Starting the service ".format(serviceName))

    return ERR





GetFreeStreamer()