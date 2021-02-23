import RPi.GPIO as GPIO
import os
import sys
import xml.etree.ElementTree as ET
from time import sleep
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '192.168.0.178'  # DTM Rpi address
host_port = 8889
posts_received = 0
post_data = ''

def appendLog(entry):
    tree = ET.parse('TrustLogv1.xml')
    root = tree.getroot()
    ct = datetime.datetime.now()
    tStamp = str(ct)
    nEl = ET.SubElement(root, 'DCMContact')
    nEl.set('timestamp', tStamp)
    nEl.text = entry
    obj_xml = ET.tostring(data)
    with open("TrustLogv1.xml", "wb") as f:
        f.write(obj_xml)

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
    str_in = '<p>' + str_in + '</p>'
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
                    <h1>Welcome to the DTM http.server v1.01</h1>
                    <p>Running on a Raspberry Pi Zero W</p>
                    <p>Current DTM GPU temperature is {}</p>
                    <form method="POST">
                        <input name="submit">
                    </form>
                    <p>Current DCM GPU temperature is UNKNOWN</p>
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
                    <title>DTM Server (Stable Page)</title>
                </head>
                <body style="width:960px; margin: 20px auto;">
                    <h1>Welcome to the DTM http.server v1.01</h1>
                    <p>Running on a Raspberry Pi Zero W</p>
                    <p>Current DTM GPU temperature is {}</p>
                    <form method="POST">
                        <input name="submit">
                    </form>
                    <p>Current DCM GPU temperature is {}</p>
            '''
            end_html = '''</body>
                             </html>'''
            
            global post_data
            temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
            dcTemp = getDCMTemp(post_data)
            dcTime = getDCMTime(post_data)
            timestamp = 'Updated: ' + dcTime
            raw_xml = 'Parsed from XML: ' + '"' + post_data + '"'
            connections = 'This was DCM Update #: ' + posts_received + 'since epoch.'
            print(makeHtmlLine(raw_xml))
            html = html + makeHtmlLine(timestamp) + makeHtmlLine(raw_xml) + makeHtmlLine(connections) + end_html
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




if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()

