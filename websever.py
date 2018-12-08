from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.write_headers()
                output = "<html><body> Hello!"
                output += "<form method = 'POST' enctype='multipart/form-data' action='/hello'>"
                output += "<h2> What would you like me to say?</h2>"
                output += "<input name='message' type = 'text'>"
                output += "<input type='submit' value='Submit'>"
                output += "</form></body></html>"
                self.write_body(output)

            elif self.path.endswith("hola"):
                self.write_headers()
                self.write_body("<html><body>Hola! <a href='/hello'>Back to Hello</a> </body></html>")

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            self.write_headers()

            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = "<html><body>"
            output += "<h2>OK, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0].decode()
            output += "<form method = 'POST' enctype='multipart/form-data' action='/hello'>"
            output += "<h2> What would you like me to say?</h2>"
            output += "<input name='message' type = 'text'>"
            output += "<input type='submit' value='Submit'>"
            output += "</form></body></html>"
            self.write_body(output)
        except Exception as e:
            print(e)

    def write_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def write_body(self, output):
        self.wfile.write(output.encode())
        print(output)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web server running on port %s")
        server.serve_forever()

    except KeyboardInterrupt:
        print("Stopping the server..")
        server.socket.close()


if __name__ == '__main__':
    main()
