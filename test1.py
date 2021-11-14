from socket import *
import requests
import threading
import sys
import os
import requests
from requests.auth import HTTPBasicAuth
from config import *
from telnetlib import Telnet
import webbrowser

server_port = sys.argv[1]
ip_addr = '127.0.0.1'
same_url = 'http://' + ip_addr + ':' + server_port

def starttab(url):
	webbrowser.open_new_tab(same_url + url)
	
	

def test_get():
	get_1 = requests.get(same_url + '/website/index.html')
	print('GET /website/index.html : ' + str(get_1.status_code))
	get_2 = requests.get(same_url + '/website/demo.png')
	print('GET /website/demo.png : ' + str(get_2.status_code))
	get_3 = requests.get(same_url + '/website/demo.pdf')
	print('GET /website/demo.pdf : ' + str(get_3.status_code))
	get_4 = requests.get(same_url + '/website/demo.jpeg')
	print('GET /website/demo.jpeg : ' + str(get_4.status_code))
	get_5 = requests.get(same_url + '/website/demo.txt')
	print('GET /website/demo.txt : ' + str(get_5.status_code))
	
		
def test_post():
	post_inp1 = {'uname': 'Apurva', 'psw':'test123'}
	post_url = same_url + '/website/dashboard.html'
	post_req1 = requests.post(post_url, post_inp1)
	print('POST /website/dashboard.html: ' + str(post_req1.status_code))

	

def test_head():
	head_1 = requests.head(same_url + '/website/index.html')
	print('HEAD /website/index.html: ' + str(head_1.status_code))
	head_2 = requests.head(same_url + '/website/login.html')
	print('HEAD /website/login.html: ' + str(head_2.status_code))
	
	
def test_put():
	data_file = "<h1>Hello World</h1>"
	put_1 = requests.put(same_url + "/demo.html", data =data_file)
	print("PUT /demo.html: " + str(put_req.status_code))
		
	
def test_delete():
	del_1 = requests.delete(same_url + "/demo.html", auth = HTTPBasicAuth(USERNAME, PASSWORD))
	print("DELETE /demo.html: " + str(delete_req.status_code))
	get_2 = requests.get(same_url + "/demo.html")
	print("GET /demo.html: " + str(get_2.status_code))	
	
	
def main_func():
	starttab(same_url + 'website/demo.png')
	starttab(same_url + 'website/demo.jpeg')
	head_th = threading.Thread(target=test_head)
	head_th.start()
	get_th = threading.Thread(target=test_get)
	get_th.start()
	'''
	post_th = threading.Thread(target=test_post)
	post_th.start()
	put_th = threading.Thread(target=test_put)
	put_th.start()
	del_th = threading.Thread(target=test_delete)
	del_th.start()
	down_th = threading.Thread(target=test_downloading_img)
	down_th.start()
	'''
	
	head_th.join()
	get_th.join()
#	post_th.join()
#	put_th.join()
#	down_th.join()
	
main_func()

