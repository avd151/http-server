#Utils required
numbers_to_months = {
    '1' : 'Jan', 
    '2' : 'Feb', 
    '3' : 'Mar',
    '4' : 'Apr',
    '5' : 'May',
    '6' : 'Jun',
    '7' : 'Jul',
    '8' : 'Aug',
    '9' : 'Sep',
    '10' : 'Oct',
    '11' : 'Nov',
    '12' : 'Dec'
}

months_to_numbers = {
    'Jan' : '1', 
    'Feb' : '2', 
    'Mar' : '3',
    'Apr' : '4',
    'May' : '5',
    'Jun' : '6',
    'Jul' : '7',
    'Aug' : '8',
    'Sep' : '9',
    'Oct' : '10',
    'Nov' : '11',
    'Dec' : '12'
}

media_types = {
    'html': 'text/html', 
    'txt': 'text/plain', 
	'jpg': 'image/jpeg', 
    'png': 'image/png', 
    'csv': 'text/csv', 
    'pdf': 'application/pdf', 
    'mp3': 'audio/mpeg',
    'mp4': 'video/mp4'
}

file_extensions = ['txt', 'html', 'jpg', 'jpeg', 'png', 'pdf', 'mp3', 'mp4']
other_than_txt_extensions = ['jpg', 'jpeg', 'png', 'mp3', 'mp4']

status_codes_messages = {
    200: 'OK', 
    201: 'Created', 
    204: 'No Content', 
    301: 'Moved Permanently', 
    304: 'Not Modified',
    400: 'Bad Request',
    401: 'Unauthorized', 
    403: 'Forbidden', 
    404: 'Not Found', 
    408: 'Request Timeout',
    411: 'Length Required', 
    413: 'Payload Too Large', 
    414: 'URI Too Long',
    415: 'Unsupported Media Type', 
    500: 'Internal Server Error', 
    501: 'Not Implemented',
    503: 'Service Unavailable',	
    505: 'HTTP Version not Supported'
}

http_methods = ['OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'CONNECT']

http_headers = [
    'Accept',
    'Accept-Charset',
    'Content-Encoding',
    'Accept-Encoding',
    'Content-Length',
    'Content-MD5',
    'Content-Type',
    'Date',
    'Host',
    'If-Modified-Since',
    'If-Range',
    'If-Unmodified-Since',
    'Range',
    'User-Agent',
    'Accept-Ranges',
    'Content-Location',
    'ETag',
    'Expires',
    'Last-Modified',
    'Location',
    'Server',
    'Set-Cookie',
    'Transfer-Encoding',
    'Connection',
    'Keep-Alive',
    'Allow',
]