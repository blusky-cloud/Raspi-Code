import urllib3
import http.client
import urllib.request
import urllib.parse
import RPi.GPIO as GPIO
import os
import sys
import xml.etree.ElementTree as ET
from time import sleep
import datetime

host_name = '192.168.0.178'  # DTM Rpi address
host_port = 8889
host_address = '192.168.0.178:8889'

def getTemp():
    traw = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    traw = traw.replace('temp=', '')
    traw = traw.replace('\n', '')
    traw = traw[:-2]
    temp = str(traw)
    return temp

temp = getTemp()
ct = datetime.datetime.now()
tStamp = str(ct)

data = ET.Element('TrustLog')
el1 = ET.SubElement(data, 'DCMContact')
el1.set('timestamp', tStamp)
el1.set('temp', temp)
el1.text = 'CONNECTION SUCCESSFUL'
#sel1.text = temp

obj_xml = ET.tostring(data)

headers = {"Content-type": "text/xml", "Accept": "text/plain"}

while True:
    sendDTM = http.client.HTTPConnection(host_name, host_port)
    sendDTM.request('POST', host_address, obj_xml, headers)
    sleep(5)

'''
http = urllib3.PoolManager()
r = http.request('POST', host_address, fields)
'''
