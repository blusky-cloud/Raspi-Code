import RPi.GPIO as GPIO
import os
from time import sleep
import http.server
import socketserver

host_name = '192.168.0.178'  # Change this to your Raspberry Pi IP address
PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Stable1 Server Starts - %s:%s" % (host_name, PORT))
    httpd.serve_forever()

