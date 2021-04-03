from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        with open('offers.json') as json_file:
            offers = json.load(json_file)
        json_string = json.dumps(offers)
        self.wfile.write(json_string.encode(encoding='utf_8'))
        return

if __name__ == '__main__':
    server = HTTPServer(('localhost', 80), RequestHandler)
    print('Starting server at http://localhost:80')
    server.serve_forever()