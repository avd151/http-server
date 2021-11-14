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

COOKIE_ID = 0
server_tcp_sock = socket(AF_INET, SOCK_STREAM)

dns_udp_sock = socket(AF_INET, SOCK_DGRAM)


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

logging.basicConfig(
    filename=LOGFILE,
    format=LOG_FORMAT,
    level=logging.INFO)
# create logger with given name, if not specified - create root logger #check
logger = logging.getLogger()

# Function to return current date


def current_date():
	curr_time = time.ctime().split(' ')  # check
	curr_time[0] = curr_time[0] + ','
	time_msg = ''.join(curr_time)
	time_msg = 'Date: ' + time_msg
	return time_msg

# Function to return last modified date of data


def modified_date(data):
	mod_time = time.ctime(os.path.getmtime(data)).split(' ')
	for i in mod_time:  # check
		if(len(i) == 0):
			mod_time.remove(i)
	mod_time[0] = mod_time[0] + ','
	time_msg = ''.join(mod_time)
	time_msg = 'Last-Modified: ' + time_msg
	return time_msg

# Function to return status codes output - in html file


def status_codes_output(status_code, serverSocket):
	if status_code == '400':
		fp = open(ROOT+'/utils/400.html', 'r')
	if status_code == '401':
		fp = open(ROOT+'/utils/401.html', 'r')
	if status_code == '403':
		fp = open(ROOT+'/utils/403.html', 'r')
	if status_code == '404':
		fp = open(ROOT+'/utils/404.html', 'r')
	if status_code == '415':
		fp = open(ROOT+'/utils/415.html', 'r')
	if status_code == '500':
		fp = open(ROOT+'/utils/500.html', 'r')
	if status_code == '503':
		fp = open(ROOT+'/utils/503.html', 'r')
	if status_code == '505':
		fp = open(ROOT+'/utils/505.html', 'r')
	file_content = fp.read()
	serverSocket.send(file_content.encode())


def handle_get_method(connectionSocket, client_request, clientList, COOKIE_ID):
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
			if file_details[1] in media_types.keys():
				file_exten = media_types[file_details[1]]                
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
			connectionSocket.send(file_content.encode())
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


def handle_head_method(connectionSocket, client_request, clientList, COOKIE_ID):
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
			if file_details[1] in media_types.keys():
				file_exten = media_types[file_details[1]]
				file_exten_msg = 'Content-Type: ' + file_exten                
				head_response.append(file_exten_msg)                
			cookie_msg = 'Set-Cookie : Id = ' + str(COOKIE_ID) + ' '            
			cookie_msg = cookie_msg + 'Max-Age = 3000'            
			head_response.append(cookie_msg)            
			head_response.append('Connection closed\n\n')            
			encoded_response = '\r\n'.join(head_response).encode()            
			connectionSocket.send(encoded_response) 
			put_msg = 'Put method successful!'
			connectionSocket.send(put_msg.encode())           
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


def handle_put_method(connectionSocket, client_request, clientList):
    # Done on command line
	file = ROOT + client_request[1]
	host_msg = 'Host: '
	connectionSocket.send(host_msg.encode())
	host_val = connectionSocket.recv(1024).decode()
	content_type_msg = 'Content-Type: '
	connectionSocket.send(content_type_msg.encode())
	file_type_val = connectionSocket.recv(1024).decode()
	content_msg = 'Content: '
	connectionSocket.send(content_msg.encode())
	content_val = connectionSocket.recv(1024).decode()
	fp = open(file, 'a')
	fp.write(content_val)
	fp.close()
	clientList.remove(connectionSocket)
	connectionSocket.close()


def handle_delete_method(connectionSocket, client_request, clientList):
	file = ROOT + client_request[1]
	username_msg = 'Enter Username: '
	connectionSocket.send(username_msg.encode())
	username_val = connectionSocket.recv(1024).decode()
	username_val = username_val.split()
	password_msg = 'Enter Password: '
	connectionSocket.send(password_msg.encode())
	password_val = connectionSocket.recv(1024).decode()
	password_val = password_val.split()
	flag = 0
	if(username_val[0] == USERNAME and password_val[0] == PASSWORD):
		flag = 1
	if(flag == 1):
		if(os.path.isfile(file)):
			os.remove(file)
			del_success_msg = 'File Deleted Successfully\n'
			connectionSocket.send(del_success_msg.encode())
		else:
			status_codes_output('404', connectionSocket)  # check
	else:
		status_codes_output('401', connectionSocket)
	clientList.remove(connectionSocket)
	connectionSocket.close()


def handle_post_method(connectionSocket, client_request, clientList):
	post_response = []
	uri_sentence = connectionSocket.recv(1024).decode()
	line = uri_sentence.split('\r\n\r\n')
	fp = fopen('post_data.txt', 'w')
	post_data = line[0].split('&')
	fp.write(post_data[0] + '\n')
	fp.write(post_data[1] + '\n')
	fp.wrie('\n')
	fp.close()
	print('{}\n {} \n'.format(post_data[0], post_data[1]))
	post_response.append('HTTP/1.1 200 OK')
	modified_date = modified_date('post_data.txt')
	post_response.append(modified_date)
	post_response.append('Server: HTTP/1.1 (Ubuntu)')
	post_response.append('Content-Language: en-US, en')
	file_size = os.path.getsize('post_data.txt')
	post_response.append('Content Length: ', str(file_size))
	post_response.append('Content-Type: text/html')
	len_response = len(post_response)
	for i in range(len_response):
		print(response[i])
	clientList.remoce(connectionSocket)
	connectionSocket.close()


def handle_all_methods(connectionSocket, addr, clientList, COOKIE_ID):
	print('in handle methods')
	data = connectionSocket.recv(1024).decode()
	client_request = data.split()
	request = 'Request: '
	address = 'Client Address: '
	port = 'Port No.: '
	logging.info('{} {} {} {} {} {}\n'.format(
        address, addr[0], port, addr[1], request, data))

	if(client_request[0] == 'GET'):
		print('in if of get')
		handle_get_method(connectionSocket, client_request, clientList, COOKIE_ID)

	if(client_request[0] == 'HEAD'):
		handle_head_method(connectionSocket, client_request, clientList, COOKIE_ID)

	if(client_request[0] == 'PUT'):
		handle_put_method(connectionSocket, client_request, clientList)

	if(client_request[0] == 'DELETE'):
		handle_delete_method(connectionSocket, client_request, clientList)

	if(client_request[0] == 'POST'):
		handle_post_method(connectionSocket, client_request, clientList)

def connect_func():
	print('in connect')
	COOKIE_ID = 0
	while(True):
		connectionSocket, addr = serverSocket.accept()
		print(connectionSocket)
		clientList.append(connectionSocket)
		if(len(clientList) <= MAX_NO_OF_REQUESTS):
			print('Connected with Client Address : ', addr)
			COOKIE_ID += 1
			try:
				print('in try')
				th1 = threading.Thread(target=handle_all_methods, args=(connectionSocket, addr, clientList, COOKIE_ID))
				th1.start()
			except:
				print('Cannot create a Thread')
		else:
			status_codes_output('503', connectionSocket)
			clientList.remove(connectionSocket)
			connectionSocket.close()


if __name__ == '__main__':
    try:
        server_port = int(sys.argv[1])
    except:
        print('Please Enter a Port Number for Server.')
        print('Usage: python3 main-http-server.py <port_number>')
        exit(1)
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', server_port))
    print(server_port)
    # except:
    #     print('Cannot start server')
    #     exit(1)
    serverSocket.listen(6)
    print('HTTP Server has started running on Port: {}'.format(server_port))
    connect_func()
    serverSocket.close()
    exit(0)







