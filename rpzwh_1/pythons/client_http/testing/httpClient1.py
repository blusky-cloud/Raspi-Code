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

ct = datetime.datetime.now()
tStamp = str(ct)
el1 = ET.Element('DCMContact')
el1.set('timestamp', tStamp)
sel1 = ET.SubElement(el1, "update")
temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
temp = temp.format(temp[5:]).encode("utf-8")
sel1.text = temp
obj_xml = ET.tostring(el1)
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
