import subprocess
import os
import threading  
import psutil
import time
from backend.dcm import ManageService, UpdateMgntDevicesLocation
from backend.models import Server, db
from backend.views import updateServerPowerState, getPowerStateFromMgnt

#================================= Threading to stop non used streamers =====================================

def StopNotUsedStreamers():
    while True:           
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
            streamerNum = str(port)[-1]
            status = ManageService('ustreamer@"'+streamerNum+'"','stop')
            time.sleep(1)
        
        time.sleep(10)
    
#================================= Threading to stop non used streamers =====================================
thread = threading.Thread(target=StopNotUsedStreamers, args=())
thread.daemon = True 
thread.start() 
print("- Streamers monitoring thread activated!")
#===============================================================================================================

def UpdateServersData():
    
    while True:
        serversList = UpdateMgntDevicesLocation()
        if serversList == -1:
            print('Error reading database')
            time.sleep(60)
        
        for server in serversList:
            dev = server.mgnt_port.split(" ")[0]
            state=getPowerStateFromMgnt(dev)
            updateServerPowerState(server.id,state)

            if state=='ON':
                server.uptime = str(int(server.uptime) + 1)
                db.session.commit()
            else:
                server.uptime = 0
                db.session.commit()

        time.sleep(60)


    #     serversCount = Server.query.count()
    #     print('entrou')
    #     print(serversCount)
    #     time.sleep(60)

#================================= Servers state and uptime thread =============================================
thread = threading.Thread(target=UpdateServersData, args=())
thread.daemon = True 
thread.start() 
print("- Servers state and uptime thread activated!")
#===============================================================================================================