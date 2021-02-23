
import os
import sys
import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
from xml.dom import minidom
from time import sleep
import datetime


workingpost = '''<TrustLog><DCMContact temp="39.5" timestamp="2021-02-23 08:37:42.187070">CONNECTION S
UCCESSFUL</DCMContact></TrustLog> '''

traw = '''temp=41.2'C'''

def getDCMTemp(xml_input):
    root = ET.fromstring(xml_input)
    DCMTemp = root[0] #DCMContact[0] is update
    print(DCMTemp.tag) 
    print(DCMTemp.attrib)
    print(DCMTemp.attrib['temp'])
    temp = float(DCMTemp.attrib['temp'])
    return temp

def getDCMTime(xml_input):
    root = ET.fromstring(xml_input)
    DCMTime = root[0] #DCMContact[0] is update
    print(DCMTime.tag) 
    print(DCMTime.attrib['timestamp'])
    timestamp = str(DCMTime.attrib['timestamp'])
    return timestamp

def makeHtmlLine(str_in):
    str_in = '<p>' + '"' + str_in +'"' + '</p>'
    return str_in

def checkXML():
    tree = ET.parse('TrustLogv2test.xml')
    root = tree.getroot()
    ct = datetime.datetime.now()
    tStamp = str(ct)
    newContact = ET.SubElement(root, 'DCMContact')
    newContact.set('timestamp', tStamp)
    newContact.set('temp', temp)
    print(root)
    print(prettify(root))
    
def appendLog(dcm_temperature, dcm_timestamp):
    tree = ET.parse('TrustLogv2test.xml')
    root = tree.getroot()
    
    dtm_time = str(datetime.datetime.now())
    newContact = ET.SubElement(root, 'DCMContact')
    newContact.set('DCM_timestamp', dcm_timestamp)
    newContact.set('DCM_emp', dcm_temperature)
    newContact.set('log_update_timestamp', dtm_time)
    
    #tree.write('TrustLogv2test.xml')
    '''
    prettyXml = prettify(root)
    prettyRoot = ET.fromstring(prettyXml)
    prettyRoot.write('TrustLogv2test.xml')
    print(pretty_xml) '''
    #print(type(tree))
    #print(tree)
    #print("now call prettify xxx")
    prettyXmlStr = prettify(root)
    #print("after prettify call xxx")
    #print(type(prettyXmlStr))
    #print(prettyXmlStr)
    prettyXmlStr = prettyXmlStr.replace('</TrustLog>', '\n</TrustLog>')
    prettyXmlStr = prettyXmlStr.replace('<TrustLog>', '\n<TrustLog>')
    #print(prettyXmlStr)
    with open('TrustLogv2test.xml', 'w') as logFile:
        print(prettyXmlStr, file=logFile)
    '''
    prettyRoot = ET.fromstring(prettyXmlStr)
    print(type(prettyRoot))
    print(prettyRoot)
    tree._setroot(prettyRoot)
    '''
    #tree.write('TrustLogv2test.xml')


    #with open("TrustLogv2test.xml", "wb") as f:
        #f.write(pretty_xml)
    
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    print("prettify function: rough_string:")
    rough_string = ET.tostring(elem, 'utf-8')
    
    print(rough_string)
    print(type(rough_string)) #bytes
    new_rough_string = rough_string.replace(b'\n', b'')
    new_rough_string = rough_string.replace(b'\t', b'')
    print(new_rough_string)
    '''
    testStr = str(rough_string)
    print(type(testStr)) #str
    testBytes = testStr.encode('utf-8')
    print(type(testBytes))
    print(testBytes)
    fakeparse = minidom.parseString(testBytes)
    testStr = testStr.replace('\n', '')
    lessRoughString = testStr.encode('utf-8')
    print(type(lessRoughString)) #bytes
    '''
    reparsed = minidom.parseString(new_rough_string)
    print(type(reparsed))
    return reparsed.toprettyxml(indent='\t', newl='')

#indent="\t", newl=''

#print("XML TEST PROGRAM. RAW:")
#print(workingpost)

print("NOW APPEND----------")
#appendLog()
#checkXML()
tTemp = str(getDCMTemp(workingpost))
tStamp = str(getDCMTime(workingpost))
appendLog(tTemp, tStamp)
print("===========APPEND COMPLETE")



'''

                    <form method="POST">
                        <input name="submit">
                    </form>
'''