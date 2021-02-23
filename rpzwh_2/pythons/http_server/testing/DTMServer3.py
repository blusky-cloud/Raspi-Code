import RPi.GPIO as GPIO
import os
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
from time import sleep
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '192.168.0.178'  # DTM Rpi address
host_port = 8889
posts_received = 0
post_data = ''


def appendLog(dcm_temperature, dcm_timestamp):
    """update the .xml log of dcm updates every 1 minute
    """
    if posts_received % 12 == 0: #because the http client program running on the dcm
                                 #submits a POST request every 5 seconds
        tree = ET.parse('TrustLogv2.xml')
        root = tree.getroot()
        dtm_time = str(datetime.datetime.now())
        newContact = ET.SubElement(root, 'DCMContact')
        newContact.set('DCM_timestamp', dcm_timestamp)
        newContact.set('DCM_emp', dcm_temperature)
        newContact.set('log_update_timestamp', dtm_time)
        prettyXmlStr = prettify(root)
        prettyXmlStr = prettyXmlStr.replace('</TrustLog>', '\n</TrustLog>')
        prettyXmlStr = prettyXmlStr.replace('<TrustLog>', '\n<TrustLog>')
        with open('TrustLogv2.xml', 'w') as logFile:
            print(prettyXmlStr, file=logFile)

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    new_rough_string = rough_string.replace(b'\n', b'')
    new_rough_string = rough_string.replace(b'\t', b'')
    reparsed = minidom.parseString(new_rough_string)
    return reparsed.toprettyxml(indent='\t', newl='')

def getDCMTemp(xml_input):
    root = ET.fromstring(xml_input)
    DCMTemp = root[0] #DCMContact[0] is update
    temp = float(DCMTemp.attrib['temp'])
    return temp

def getDCMTime(xml_input):
    root = ET.fromstring(xml_input)
    DCMTime = root[0] #DCMContact[0] is update
    timestamp = str(DCMTime.attrib['timestamp'])
    return timestamp

def makeHtmlLine(str_in):
    str_in = '<p style="text-indent: 40px">' + str_in + '</p>'
    return str_in

def makeHtmlText(str_in):
    str_in = '<textarea rows="2" cols="100" style="border:double 2px blue;">' + str_in + '</textarea>'
    return str_in

class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        if posts_received == 0:
            print("NO POST REQUESTS")
            html = '''
                <html>
                <head>
                    <title>DTM Server (Stable Page)</title>
                </head>
                <body style="width:960px; margin: 20px auto;">
                    <h1 style="text-indent: 40px">Welcome to the DTM http.server v1.01</h1>
                    <p style="text-indent: 40px">Running on a Raspberry Pi Zero W</p>
                    <p style="text-indent: 40px">Current DTM GPU temperature is {}</p>
                    <hr><br><br>
                    <p style="text-indent: 40px">Current DCM GPU temperature is UNKNOWN</p>
                </body>
                </html>
            '''
            temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
            self.do_HEAD()
            self.wfile.write(html.format(temp[5:]).encode("utf-8"))
        
        if posts_received > 0:
            print("POST REQUEST: UPDATE HTML PAGE")
            html = '''
                <html>
                <head>
                    <title>DTM Server Display </title>
                </head>
                <body style="width:960px; margin: 20px auto;">
                    <h1 style="text-indent: 40px">Welcome to the DTM http.server v1.02</h1>
                    <p style="text-indent: 40px">Running on a Raspberry Pi Zero W</p>
                    <p style="text-indent: 40px">Current DTM GPU temperature is {}</p>
                    <hr><br><br>
                    <p style="text-indent: 40px"><b>Current DCM GPU temperature is {}'C</b></p>
            '''
            end_html = '''</body>
                             </html>'''
            
            global post_data
            temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
            dcTemp = getDCMTemp(post_data)
            dcTime = getDCMTime(post_data)
            timestamp = '<b>Updated: ' + dcTime + '</b>'
            xmlTitle = '<i>Data parsed from the following (DCM generated) XML:</i>'
            raw_xml = str(post_data) 
            connections = 'From DCM Update #: ' + str(posts_received) + ' since DTM Server epoch'
            
            html = html + makeHtmlLine(timestamp) + makeHtmlLine(xmlTitle) + makeHtmlText(raw_xml) + makeHtmlLine(connections) + end_html
            self.do_HEAD()
            self.wfile.write(html.format(temp[5:], dcTemp).encode("utf-8"))
            
    def do_POST(self):
        global posts_received 
        global post_data
        posts_received += 1
        post_data = self.rfile.read().decode("utf-8")  # Get the data
        print(" POST REQUEST RECEIVED. raw:")
        print(post_data)
        print(posts_received)
        local_temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        dcm_temp = str(getDCMTemp(post_data)) #getDCMTemp returns a float
        dcm_time = getDCMTime(post_data) #returns a string
        appendLog(dcm_temp, dcm_time)


if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()

