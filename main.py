import os,  json,  time
from http.server import SimpleHTTPRequestHandler, HTTPServer, BaseHTTPRequestHandler

def logattendence(data):
    print(data)
    filetowrite = open("/home/o/Digital_Attendence_System/backend_dyna_files/c1p1.js", "w")
    filetowrite.write("const=presence"+" "+json.dumps(data))

class main(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/room1':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('/home/o/Digital_Attendence_System/frontend_files/room1.htm', 'rb') as file:
                self.wfile.write(file.read())
        if self.path == '/class1.js':
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            with open('/home/o/Digital_Attendence_System/backend_static_files/class1.js', 'rb') as file:
                self.wfile.write(file.read())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'status': 'success', 'received': data}
        self.wfile.write(json.dumps(response).encode('utf-8'))
        logattendence(data)

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, main)
    httpd.serve_forever()
