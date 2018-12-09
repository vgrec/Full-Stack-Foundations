from http.server import BaseHTTPRequestHandler, HTTPServer
from restaurants_repository import RestaurantsRepository
import cgi


class WebServerHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.show_restaurants()
            elif self.path.endswith("hola"):
                pass
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            pass
        except Exception as e:
            print(e)

    def write_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def write_body(self, output):
        self.wfile.write(output.encode())
        print(output)

    def show_restaurants(self):
        self.write_headers()
        repository = RestaurantsRepository()

        output = "<html><body>"
        restaurants = repository.get_restaurants()
        for restaurant in restaurants:
            output += restaurant.name
            output += "<br/>"
        output += "</body></html>"

        self.write_body(output)
        print()


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("Stopping the server..")
        server.socket.close()


if __name__ == '__main__':
    main()
