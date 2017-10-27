from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):
  def valid_text_response(self, code):
    self.send_response(code)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def wrap_html_body(self, content):
    return "<html><body>" + content + "</body></html>"

  def form_message(self):
    return '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''

  def form_add_restaurant(self):
    return '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Please enter the new restaurant name:</h2><input name="message" type="text" placeholder = "New Restaurant Name"><input type="submit" value="Create"> </form>'''

  def do_GET(self):
    try:
      if self.path.endswith("/hello"):
        self.valid_text_response(200)
        output = ""
        output += "Hello!"
        output += self.form_message()
        message = self.wrap_html_body(output)
        self.wfile.write(message)
        print message
        return

      if self.path.endswith("/hola"):
        self.valid_text_response(200)
        output = ""
        output += "&#161Hola! <a href='/hello'>Back to Hello</a>"
        output += self.form_message()
        message = self.wrap_html_body(output)
        self.wfile.write(message)
        print message
        return

      if self.path.endswith("/restaurants"):
        self.valid_text_response(200)
        output = ""
        output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"

        restaurants = session.query(Restaurant).all()
        for restaurant in restaurants:
          output += restaurant.name
          output += "</br>"
          output += "<a href='#'>Edit</a>"
          output += "</br>"
          output += "<a href='#'>Delete</a>"
          output += "</br>" * 2
        message = self.wrap_html_body(output)
        self.wfile.write(message)
        print message
        return

      if self.path.endswith("/restaurants/new"):
        self.valid_text_response(200)
        output = ""
        output += self.form_add_restaurant()
        message = self.wrap_html_body(output)
        self.wfile.write(message)
        print message
        return

    except IOError:
      self.send_error(404, "File Not Found %s" % self.path)

  def do_POST(self):
    try:
      if self.path.endswith("/restaurants/new"):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

        if ctype == 'multipart/form-data':
          fields = cgi.parse_multipart(self.rfile, pdict)
          message_content = fields.get('message')

          new_restaurant = Restaurant(name = message_contenti[0])
          session.add(new_restaurant)
          session.commit()

          self.send_response(301)
          self.send_header('Content-type', 'text/html')
          self.send_header('Location', '/restaurants')
          self.end_headers()

    except:
      pass

def main():
  try:
    port = 8080
    server = HTTPServer(('', port), webServerHandler)
    print "Web server running on port %s" % port
    server.serve_forever()

  except KeyboardInterrupt:
    print "^C entered, stopping web server ..."
    server.socket.close()

if __name__ == '__main__':
  main()
