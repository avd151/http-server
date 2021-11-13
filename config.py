import os

#Timeout (in seconds) for Thread Request
TIMEOUT = 30

#Max Thread Requests Server can support
MAX_NO_OF_REQUESTS = 30

#Max URI Length of HTTP Request the Server can Support
MAX_URI_LENGTH = 100

#Max Size of Payload of data the Server can Support (in bytes)
MAX_PAYLOAD_LEN = 1073741824 #1GB

#Document Root of Server = Current Working Directory
ROOT = os.getcwd()

#Log File location #access.log file of server
LOGFILE = ROOT + '/server_logfile.log'

#Logfile will be expired (deleted) after this time (in seconds)
LOGFILE_EXP_TIME = 5184000 #60 days = 5184000 seconds

#Log format 
LOG_FORMAT = '%(asctime)s : %(uri)s : %(message)s'

#Demo Username and Password for Testing Delete
USERNAME = 'test1'
PASSWORD = 'test123'


