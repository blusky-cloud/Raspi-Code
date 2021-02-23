import urllib3
import http.client
import RPi.GPIO as GPIO
import os
import sys
import xml.etree.ElementTree as ET
from time import sleep
import datetime

host_name = '192.168.0.178'  # DTM Rpi address
host_port = 8889
host_address = '192.168.0.178:8889'

temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
temp = temp.format(temp[5:]).encode("utf-8")
temp = str(temp)
ct = datetime.datetime.now()
tStamp = str(ct)

data = ET.Element('TrustLog')
el1 = ET.SubElement(data, 'DCMContact')
el1.set('timestamp', tStamp)
sel1 = ET.SubElement(el1, "update")
sel1.text = temp

obj_xml = ET.tostring(data)

params = urllib.parse.urlencode(obj_xml)
headers = {"Content-type": "text/xml", "Accept": "text/plain"}

while True:
    sendDTM = http.client.HTTPConnection(host_name, host_port)
    sendDTM.request('PUT', obj_xml, headers)
    sleep(5)

'''
http = urllib3.PoolManager()
r = http.request('POST', host_address, fields)
'''
