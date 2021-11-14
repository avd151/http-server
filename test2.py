import webbrowser, os, sys
from socket import *
import requests
import http
import urllib

port = sys.argv[1]

IP = '127.0.0.1'

same_url_part = "http://" + 	IP + ":" + port 

def starttab(url = (same_url_part)):
    webbrowser.open_new_tab(url)

def main():
    starttab(same_url_part + "/website/demo.mp3")
    starttab(same_url_part + "/website/demo.mp4")
    starttab(same_url_part + "/website/demo.html")
    starttab(same_url_part + "/website/demo.png")
    starttab(same_url_part + "/website/demo.jpeg")
    starttab(same_url_part + "/website/demo.pdf")
    starttab(same_url_part + "/website/demo.txt")

if __name__ == "__main__":
    main()