from http.server import BaseHTTPRequestHandler, HTTPServer
from restaurants_repository import RestaurantsRepository
import cgi


class WebServerHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.show_restaurants_page()
                return

            if self.path.endswith("/restaurants/new"):
                self.show_add_new_restaurant_page()
                return

            if self.path.endswith("/edit"):
                self.show_edit_page(self.path)
                return
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.create_new_restaurant()
                return

            if self.path.endswith("/edit"):
                self.edit_restaurant(self.path)
                return

        except Exception as e:
            print(e)

    def write_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def write_body(self, output):
        self.wfile.write(output.encode())

    def show_restaurants_page(self):
        self.write_headers()
        repository = RestaurantsRepository()

        output = "<html><body>"
        output += "<h3><a href='/restaurants/new'>Add a new restaurant</a></h3>"
        output += "<br/><br/>"
        restaurants = repository.get_restaurants()
        for restaurant in restaurants:
            output += restaurant.name
            output += "<br/>"
            output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
            output += "<br/>"
            output += "<a href='#'>Delete</a>"
            output += "<br/><br/>"
        output += "</body></html>"

        self.write_body(output)

    def show_add_new_restaurant_page(self):
        self.write_headers()
        output = "<html><body>"
        output += "<h3>Add a new restaurant</h3>"
        output += "<br/><br/>"
        output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/new'>"
        output += "<h2> What would you like me to say?</h2>"
        output += "<input name='message' type = 'text'>"
        output += "<input type='submit' value='Submit'>"
        output += "</form>"
        output += "</body></html>"

        self.write_body(output)

    def show_edit_page(self, path):
        self.write_headers()
        repository = RestaurantsRepository()

        restaurant_id = path[len("/restaurants/"): path.find("/edit")]
        restaurant = repository.get_restaurant_by_id(restaurant_id)

        output = "<html><body>"
        output += "<h3>%s</h3>" % restaurant.name
        output += "<br/><br/>"
        output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurant_id
        output += "<input name='message' type = 'text' placeholder='%s'>" % restaurant.name
        output += "<input type='submit' value='Rename'>"
        output += "</form>"
        output += "</body></html>"

        self.write_body(output)

    def create_new_restaurant(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = fields.get('message')
            repository = RestaurantsRepository()
            repository.new_restaurant(messagecontent[0].decode())

        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/restaurants')
        self.end_headers()

    def edit_restaurant(self, path):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            new_name = fields.get('message')
            restaurant_id = path[len("/restaurants/"): path.find("/edit")]

            repository = RestaurantsRepository()
            repository.update_restaurant(restaurant_id, new_name[0].decode())

        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/restaurants')
        self.end_headers()


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
