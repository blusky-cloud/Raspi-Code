import RPi.GPIO as GPIO
import os
import sys
import xml.etree.ElementTree as ET
from time import sleep
import datetime

print("CREATING TrustLogv1 XML FILE")
ct = datetime.datetime.now()
tStamp = str(ct)

data = ET.Element('TrustLog')
el1 = ET.SubElement(data, 'DCMContact')
el1.set('timestamp', tStamp)
sel1 = ET.SubElement(el1, "update")
sel1.text = 'FILE CREATED'

obj_xml = ET.tostring(data)
with open("TrustLogv1.xml", "wb") as f:
    f.write(obj_xml)