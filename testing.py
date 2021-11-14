import sys
import os
import webbrowser
from socket import *

ROOT = os.getcwd()
# serverSock = socket(AF_INET, SOCK_DGRAM)
port = sys.argv[1]
#port = '9000'
IP = '127.0.0.1'
uri = 'localhost:'+ port

def open_tab(url):
    webbrowser.open_new_tab(url)

open_tab(uri + '/website/index.html')
