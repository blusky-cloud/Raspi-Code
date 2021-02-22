import RPi.GPIO as GPIO
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

print("webserver1 INITIATION")

host_name = '192.168.0.178'    # Change this to your Raspberry Pi IP address
host_port = 8000
server_active = True

#class MyServer(BaseHTTPRequestHandler):

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
        server_address = (host_name, host_port)
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()

while server_active:
        run
        print("keep running? y/n")
        choice = str(input())
        if choice != 'y':
                server_active = False

