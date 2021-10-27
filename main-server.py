

import os
import socket
import mimetypes


class TCPServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
    #Start TCP Server
    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)
        print("Listening at", s.getsockname())
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            data = conn.recv(1024)
            response = self.handle_request(data)
            conn.sendall(response) 
            conn.close()

    #This method is overriden in HTTPServer Subclass, where it handles request and returns repsonse accordingly
    def handle_request(self, data):
        return data


class HTTPServer(TCPServer):
    headers = {
        'Server': 'CrudeServer',
        'Content-Type': 'text/html',
    }

    content_types = {
        'html': 'text/html', 
        'txt': 'text/plain', 
	    'jpg': 'image/jpeg', 
        'png': 'image/png', 
        'csv': 'text/csv', 
        'pdf': 'application/pdf', 
        'mp3': 'audio/mpeg',
        'mp4': 'video/mp4'
    }

    status_codes = {
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

    def handle_request(self, data):
        """Handles incoming requests"""
        request = HTTPRequest(data)  #Parse HTTP Request according to data
        try:
            # Call the corresponding handler method for the current
            # request's method
            handler = getattr(self, 'handle_%s' % request.method)
        except AttributeError:
            handler = self.HTTP_501_handler()
        response = handler(request)
        return response

    def response_line(self, status_code):
        reason = self.status_codes[status_code]
        response_line = 'HTTP/1.1 %s %s\r\n' % (status_code, reason)

        return response_line.encode()

    def response_headers(self, extra_headers=None):
        headers_copy = self.headers.copy()
        if extra_headers:
            headers_copy.update(extra_headers)
        headers = ''
        for h in headers_copy:
            headers += '%s: %s\r\n' % (h, headers_copy[h])
        return headers.encode()  # convert str to bytes

    def handle_OPTIONS(self, request):
        """Handler for OPTIONS HTTP method"""
        response_line = self.response_line(200)
        extra_headers = {'Allow': 'OPTIONS, GET'}
        response_headers = self.response_headers(extra_headers)
        blank_line = b'\r\n'
        return b''.join([response_line, response_headers, blank_line])

    # Handler for GET HTTP method
    def handle_GET(self, request):
        path = request.uri.strip('/')  # remove slash from URI 
        if not path:
            path = 'index.html'

        if os.path.exists(path) and not os.path.isdir(path): 
            response_line = self.response_line(200)

            # find out a file's MIME type
            content_type = mimetypes.guess_type(path)[0] or 'text/html'

            extra_headers = {'Content-Type': content_type}
            response_headers = self.response_headers(extra_headers)

            with open(path, 'rb') as f:
                response_body = f.read()
        else:
            response_line = self.response_line(404)
            response_headers = self.response_headers()
            response_body = b'<h1>404 Not Found</h1>'

        blank_line = b'\r\n'

        response = b''.join(
            [response_line, response_headers, blank_line, response_body])

        return response

    def HTTP_501_handler(self, request):
        """Returns 501 HTTP response if the requested method hasn't been implemented."""

        response_line = self.response_line(status_code=501)

        response_headers = self.response_headers()

        blank_line = b'\r\n'

        response_body = b'<h1>501 Not Implemented</h1>'

        return b"".join([response_line, response_headers, blank_line, response_body])


class HTTPRequest:
    """Parser for HTTP requests. 
    Instances of this class have the following attributes:
        self.method: The current HTTP request method sent by client (string)
        self.uri: URI for the current request (string)
        self.http_version = HTTP version used by  the client (string)
    """

    def __init__(self, data):
        self.method = None
        self.uri = None
        self.http_version = '1.1'  # default to HTTP/1.1 if request doesn't provide a version

        # call self.parse method to parse the request data
        self.parse(data)

    def parse(self, data):
        lines = data.split(b'\r\n')
        request_line = lines[0]  # request line is the first line of the data
        words = request_line.split(b' ')
        self.method = words[0].decode()

        if len(words) > 1:
            self.uri = words[1].decode()

        if len(words) > 2:
            self.http_version = words[2]


if __name__ == '__main__':
    server = HTTPServer()
    server.start()
