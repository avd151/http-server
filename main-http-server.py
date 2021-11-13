from socket import *
import os
import sys
import mimetypes
from config import *
from lib import *
import time
import datetime
import logging
import random
import threading


dns_udp_sock = socket(AF_INET, SOCK_DGRAM)
server_tcp_sock = socket(AF_INET, SOCK_STREAM)


def find_ip_address():
    try:
        dns_udp_sock.connect('8.8.8.8', 8000)  # find our why 8000
        # 0- IP addr, 1 - port no. (returns a tuple)
        ip_address = dns_udp_sock.getsockname()[0]
    except:
        ip_address = '127.0.0.1'
    dns_udp_sock.close()
    return ip_address


client_ip_address = str(find_ip_address())  # ip address of host or client
# print(client_ip_address)

logging.BasicConfig(
    filename=LOGFILE,
    format=LOG_FORMAT,
    level=logging.INFO)
# create logger with given name, if not specified - create root logger #check
logger = logging.getLogger()

# Function to return current date
def current_date():
    curr_time = time.ctime().split(' ')  # check
    curr_time[0] = curr_time[0] + ','
    time_msg = '' + curr_time
    time_msg = 'Date: ' + time_msg
    return time_msg

# Function to return last modified date of data
def modified_date(data):
    mod_time = time.ctime(os.path.getmtime(data)).split(' ')
    for i in mod_time:  # check
        if(len(i) == 0):
            mod_time.remove(i)
        mod_time[0] = mod_time[0] + ','
        time_msg = '' + mod_time
        time_msg = 'Last-Modified: ' + time_msg
        return time_msg

# Function to return status codes output - in html file
def status_codes_output(status_code, serverSocket):
    fp = ''
    if status_code == '400':
        fp = open(ROOT+'/utils/400.html', 'r')
    elif status_code == '401':
        fp = fp = open(ROOT+'/utils/401.html', 'r')
    elif status_code == '403':
        fp = fp = open(ROOT+'/utils/403.html', 'r')
    elif status_code == '404':
        fp = fp = open(ROOT+'/utils/404.html', 'r')
    elif status_code == '415':
        fp = fp = open(ROOT+'/utils/415.html', 'r')
    elif status_code == '500':
        fp = fp = open(ROOT+'/utils/500.html', 'r')
    elif status_code == '503':
        fp = fp = open(ROOT+'/utils/503.html', 'r')
    elif status_code == '505':
        fp = fp = open(ROOT+'/utils/505.html', 'r')
    file_content = fp.read()
    serverSocket.send(file_content.encode())


def handle_get_request(connectionSocket, client_request, clientList):
    get_response = []
    data_element = ROOT + client_request[1]
    if(os.path.isfile(data_element)):
        if(os.access(data_element, os.W_OK) and os.access(data_element, os.R_OK)):
            get_response.append('HTTP/1.1 200 OK')
            get_response.append(current_date())
            get_response.append('Server: HTTP/1.1')
            get_response.append(modified_date(data_element))
            element_size = os.path.getsize(data_element)
            elem_size_str = str(element_size)
            elem_size = 'Content-Length: ' + elem_size_str
            get_response.append(elem_size)
            file_details = os.path.splitext(data_element)
            if file_details[1] in file_extension.keys():
                file_exten = file_extension[file_ext[1]]
                file_exten_msg = 'Content-Type: ' + file_exten
                get_response.append(file_exten_msg)
            cookie_msg = 'Set-Cookie : Id = ' + str(COOKIE_ID) + ' '
            cookie_msg = cookie_msg + 'Max-Age = 3000'
            get_response.append(cookie_msg)
            get_response.append('Connection closed\n\n')
            fp = open(data_element, 'r')
            file_content = fp.read()
            encoded_response = '\r\n'.join(get_response).encode()
            connectionSocket.send(encoded_response)
            connectionsocket.send(file_content.encode())
            clientList.remove(connectionSocket)
            connectionSocket.close()
        else:
            status_codes_output('403', connectionSocket)
            clientList.remove(connectionSocket)
            connectionSocket.close()
    else:
        status_codes_output('404', connectionSocket)
        clientList.remove(connectionSocket)
        connectionSocket.close()


def handle_head_request(connectionSocket, client_request, clientList):
    head_response = []
    data_element = ROOT + client_request[1]
    if(os.path.isfile(data_element)):
        if(os.access(data_element, os.W_OK) and os.access(data_element, os.R_OK)):
            head_response.append('HTTP/1.1 200 OK')
            head_response.append(current_date())
            head_response.append('Server: HTTP/1.1')
            head_response.append(modified_date(data_element))
            element_size = os.path.getsize(data_element)
            elem_size_str = str(element_size)
            elem_size = 'Content-Length: ' + elem_size_str
            head_response.append(elem_size)
            file_details = os.path.splitext(data_element)
            if file_details[1] in file_extension.keys():
                file_exten = file_extension[file_ext[1]]
                file_exten_msg = 'Content-Type: ' + file_exten
                head_response.append(file_exten_msg)
            cookie_msg = 'Set-Cookie : Id = ' + str(COOKIE_ID) + ' '
            cookie_msg = cookie_msg + 'Max-Age = 3000'
            head_response.append(cookie_msg)
            head_response.append('Connection closed\n\n')
            encoded_response = '\r\n'.join(head_response).encode()
            connectionSocket.send(encoded_response)
            clientList.remove(connectionSocket)
            connectionSocket.close()
        else:
            status_codes_output('403', connectionSocket)
            clientList.remove(connectionSocket)
            connectionSocket.close()
    else:
        status_codes_output('404', connectionSocket)
        clientList.remove(connectionSocket)
        connectionSocket.close()

def handle_all_methods(connectionSocket, addr, clientList, COOKIE_ID):
    data = connectionSocket.recv(1024).decode()
    client_request = data.split()
    request = 'Request: '
    address = 'Client Address: '
    port = 'Port No.: '
    logging.info('{} {} {} {} {} {}\n'.format(
        address, addr[0], port, addr[1], request, data))

    if(client_request[0] == 'GET'):
        handle_get_request(connectionSocket, client_request, clientList)

    elif(client_request[0] == 'HEAD'):
        handle_head_request(connectionSocket, client_request, clientList)

    elif(client_request[0] == 'POST'):
        pass

    elif(client_request[0] == 'PUT'):
        pass

    elif(client_request[0] == 'DELETE'):
        pass





