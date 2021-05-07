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
        tree = ET.parse('TrustLogv2.xml') #create xml tree from file contents
        root = tree.getroot() #ID root of tree (TrustLog)
        dtm_time = str(datetime.datetime.now()) #get timestamp of this moment
        newContact = ET.SubElement(root, 'DCMContact') #add element (instance of DCM contacting DTM) to the tree
        newContact.set('DCM_timestamp', dcm_timestamp) #time from xml sent from DCM in POST
        newContact.set('DCM_temp', dcm_temperature) #temp from xml sent from DCM in POST
        newContact.set('log_update_timestamp', dtm_time) #DTM time
        prettyXmlStr = prettify(root) #new string made using prettify()
        prettyXmlStr = prettyXmlStr.replace('</TrustLog>', '\n</TrustLog>') #Re-newline the tree close                                        
        prettyXmlStr = prettyXmlStr.replace('<TrustLog>', '\n<TrustLog>') #re-newline the tree open, the prettify() strips them for some reason
        with open('TrustLogv2.xml', 'w') as logFile: #open log and write
            print(prettyXmlStr, file=logFile)

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8') #encode xml object as bytes
    new_rough_string = rough_string.replace(b'\n', b'') #otherwise the ElementTree methods add newlines to the whole file each log update
    new_rough_string = rough_string.replace(b'\t', b'') # the b'' is because this is a <class 'bytes'> not <class 'string'>
    reparsed = minidom.parseString(new_rough_string) #takes bytes as arg, produces Document object
    return reparsed.toprettyxml(indent='\t', newl='') #returns a string, the args are super finnicky

def getDCMTemp(xml_input):
    """Return the DCM temp as float from the parsed xml msg
    """
    root = ET.fromstring(xml_input)
    DCMTemp = root[0] #root[0] is the DCMUpdate
    temp = float(DCMTemp.attrib['temp']) # DCMTemp.attrib['temp'] returns the attribue matching key 'temp', then convert to float
    return temp

def getDCMTime(xml_input):
    """Return the DCM time as string from the parsed xml msg
    """
    root = ET.fromstring(xml_input)
    DCMTime = root[0] #DCMContact[0] is update
    timestamp = str(DCMTime.attrib['timestamp']) # DCMTemp.attrib['timestamp'] returns the attribue matching key 'temp', then convert to float
    return timestamp

def makeHtmlLine(str_in):
    """add formatting for a "paragraph" in html to a string
    """
    str_in = '<p style="text-indent: 40px">' + str_in + '</p>'
    return str_in

def makeHtmlText(str_in):
    """add formatting for an html textarea to a string
    """
    str_in = '<textarea rows="2" cols="100" style="border:double 2px blue;">' + str_in + '</textarea>'
    return str_in

class MyServer(BaseHTTPRequestHandler):
    """server derived from python standard library BASEHTTPRequestHandler object, custom handlers
        for HEAD, GET, POST, and redirect interactions
    """

    def do_HEAD(self):
        """HEAD method type, sends to client
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers() #need to call end_headers() to actually send the headers

    def _redirect(self, path):
        """redirect method type
        """
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        """GET method type, updates the "served" html page that you can access from a browser 
            on a local network with [ip address 00.00.00.00 blah]:[port num, 4 digits, matching encoded] 
            copy pasted to url in browser
        """
        if posts_received == 0: #if the DCM has not made contact via POST request
            print("NO POST REQUESTS")
            #the below is the html string which is the webpage visible in browser
            html = '''
                <html>
                <head>
                    <title>DTM Server (Stable Page)</title>
                </head>
                <body style="width:960px; margin: 20px auto;">
                    <h1 style="text-indent: 40px">Welcome to the DTM http.server v1.03</h1>
                    <p style="text-indent: 40px">Running on a Raspberry Pi Zero W</p>
                    <p style="text-indent: 40px">Current DTM GPU temperature is {}</p>
                    <hr><br><br>
                    <p style="text-indent: 40px">Current DCM GPU temperature is UNKNOWN</p>
                </body>
                </html>
            '''
            temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read() #measure temp through raspi linux shell
            self.do_HEAD()
            self.wfile.write(html.format(temp[5:]).encode("utf-8"))
        
        if posts_received > 0: #if the DCM has made contact via POST request
            print("POST REQUEST: UPDATE HTML PAGE")
            html = '''
                <html>
                <head>
                    <title>DTM Server Display </title>
                </head>
                <body style="width:960px; margin: 20px auto;">
                    <h1 style="text-indent: 40px">Welcome to the DTM http.server v1.03</h1>
                    <p style="text-indent: 40px">Running on a Raspberry Pi Zero W</p>
                    <p style="text-indent: 40px">Current DTM GPU temperature is {}</p>
                    <hr><br><br>
                    <p style="text-indent: 40px"><b>Current DCM GPU temperature is {}'C</b></p>
            '''
            end_html = '''</body>
                             </html>'''
            
            global post_data
            temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read() #current system temp
            dcTemp = getDCMTemp(post_data) #parse xml for dcm temp
            dcTime = getDCMTime(post_data) #parse xml for dcm time
            timestamp = '<b>Updated: ' + dcTime + '</b>' #html bold formattin for posting
            xmlTitle = '<i>Data parsed from the following (DCM generated) XML:</i>' #html italicized formatting
            raw_xml = str(post_data) #generate string from xml data sent from dcm client in last POST request
            connections = 'From DCM Update #: ' + str(posts_received) + ' since DTM Server epoch' #update connection num
            #the below line just concantenates strings for the wfile.write() function, the xml has to go in an html textarea, otherwise it won't be displayed
            html = html + makeHtmlLine(timestamp) + makeHtmlLine(xmlTitle) + makeHtmlText(raw_xml) + makeHtmlLine(connections) + end_html
            self.do_HEAD() #call the HEAD method, which sends headers to the client
            self.wfile.write(html.format(temp[5:], dcTemp).encode("utf-8")) #write the formatted (to add temp data from dtm and dcm) html string (encoded) to client
            
    def do_POST(self):
        """POST method type
            the http.client is running on a DCM on the network, that client
            submits requests with 'POST', which contain xml 
            rfile.read().decode() then decodes that msg
            and saves it to a global string var 
        """
        global posts_received #global keyword needed to modify the var, there were errors declaring as 
                              #class data members
        global post_data
        posts_received += 1 #iterate count of POST requests received
        post_data = self.rfile.read().decode("utf-8")  # Get the data
        print(" POST REQUEST RECEIVED. raw:")
        print(post_data)
        print(posts_received)
        dcm_temp = str(getDCMTemp(post_data)) #getDCMTemp returns a float
        dcm_time = getDCMTime(post_data) #returns a string
        appendLog(dcm_temp, dcm_time) #appends the .xml log 

"""
this is main, just run the server
"""
if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()

