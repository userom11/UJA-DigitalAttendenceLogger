import os,  json, time, re
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, HTTPServer, BaseHTTPRequestHandler

def getime(type):
    now = datetime.now()
    year = now.year
    month = now.month
    date = now.day
    timesecs = (now.hour * 3600) + (now.minute * 60)
    terms =( json.loads( re.search(r'\{.*\}', open("backend_static_files/termdates.js", "r").read() ).group(0)) )["datesecs"]
    for n in range(0,3):
        if timesecs >= terms[n] and timesecs < terms[n+1]:
            current_term=n # term 1 to 4 (programming numbers, 0 to 3)
            break
    january_first = datetime(year, 1, 1).weekday()
    termstartday =terms[n]//86400
    currentday =(time.time())//86400
    p = (termstartday+january_first)%7
    current_term_day = currentday - termstartday +1
    current_term_week = (current_term_day -p +1)/7
    periods =( json.loads( re.search(r'\{.*\}', open("backend_static_files/periodtimes.js", "r").read() ).group(0)) )["times"]
    for x in range(0,12):
        if timesecs >= periods[x] and timesecs < periods[x+1]:
            current_period=x # period 1 to 13 (breaks, assembly, block session counts as a period) (programming number system: 0 to 12)
            break
    if type=="termweek":
        return termweek
    if type=="current_period":
        if current_period:
            return current_period


def logattendence(data):
    print(data)
    termweek = getime("termweek")
    currentperiod = getime("currentperiod")
    weekday = now.weekday()
    filetowrite = open(f"backend_dyna_files/week{termweek}/{weekday+1}/c1p1.js", "w")
    filetowrite.write("const presence="+" "+json.dumps(data))

class main(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/room1':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('frontend_files/room1.htm', 'rb') as file:
                self.wfile.write(file.read())
        if self.path == '/view':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open ('frontend_files/view.htm', 'rb') as file:
                self.wfile.write(file.read())
        if self.path == '/class1.js':
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            with open('backend_static_files/class1.js', 'rb') as file:
                self.wfile.write(file.read())
        if self.path == '/todayclass1':
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            # with open(f"backend_dyna_files/week{termweek}/{weekday+1}/c1p{current_period}.js", 'rb') as file:
            with open("backend_dyna_files/c1p2.js", 'rb') as file:
                self.wfile.write(file.read())
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        self.send_response(200)
        self.send_header('Content-type', 'application/javascript')
        self.end_headers()
        response = {'status': 'success', 'received': data}
        self.wfile.write(json.dumps(response).encode('utf-8'))
        logattendence(data)

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, main)
    httpd.serve_forever()
