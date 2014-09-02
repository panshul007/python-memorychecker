'''
Created on Oct 31, 2013

@author: panshul
'''

from sys import argv
import requests
import time
import string
from mainpackage.EmailUtil import sendServerAlertMail
from multiprocessing import Process

panshul = "panshul@innoplexia.com"
christian = "christian@innoplexia.com"
rene = "rene@innoplexia.com"
hefner = "joachim.hefner@verivox.com"
philipp = "philipp.walser@verivox.com"
navid = "navid.bazzazzadeh@verivox.com"

recepients = [panshul, christian, rene, hefner, philipp, navid]

#machineName, address = argv

machineName, address = "Data gateway","vsrest.ixurl.de:8080"
#machineName, address = "Data gateway","localhost:8080"

def checkConnection(address):
    try:
        requestString = format('http://%s/datagateway/status' %(address))
        response = requests.get(requestString,auth=('verivox','verivoxuser'))
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False    

def requestStatus(address):
    requestString = format('http://%s/datagateway/status/jvm' %(address))
    response = requests.get(requestString,auth=('verivox','verivoxuser'))
    #print response.status_code
    return response
    
def verifyStatusCode(response):
    if response.status_code!=200:
        return False
    return True

# response = "Max heap space, Current total heap space, used memory, free memory"
def getValuesFromResponse(response,checktime):
    jvmStatus = response.text[1:len(response.text)-1].split(',')
    maxHeapSpace =  float(string.strip(jvmStatus[4],'"'))
    currentHeapSpace = float(string.strip(jvmStatus[5],'"'))
    usedMemory = float(string.strip(jvmStatus[6],'"'))
    freeMemory = float(string.strip(jvmStatus[7],'"'))
    print format("%r : Max heap space: %r   Current total heap space: %r  used memory: %r   free memory: %r" %(checktime,maxHeapSpace,currentHeapSpace,usedMemory,freeMemory))
    return maxHeapSpace,currentHeapSpace,usedMemory,freeMemory


def verifyFreeHeapSpace(currentHeapSpace, freeMemory):
    freePercent = (freeMemory/currentHeapSpace)*100.0
    if freePercent<20.0:
        return False
    return True


def verifyJVMStatus(response,checkTime):
    maxHeapSpace,currentHeapSpace,usedMemory,freeMemory = getValuesFromResponse(response,checkTime)
    if maxHeapSpace==currentHeapSpace or maxHeapSpace<currentHeapSpace:
        return verifyFreeHeapSpace(currentHeapSpace,freeMemory)
    return True

def doWork():
    while True:
        checkTime = time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())
        if checkConnection(address):
            response = requestStatus(address)
            if verifyJVMStatus(response,checkTime)!=True:
                print "Send Alert Mail"
                
            else:
                print "Rest Server Stable"
        else:
            print format("%r : Send Connection Fail Alert Mail" %(checkTime))
            dsf=[]
            sendServerAlertMail(dsf,recepients,machineName,'connection')
        time.sleep((60*60))

p = Process(target=doWork)
p.start()    
#doWork()