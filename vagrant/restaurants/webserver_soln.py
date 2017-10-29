from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import re

from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):
  def _send_text_header(self, code):
    self.send_response(code)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def _send_text_header_with_location(self, code, location='/restaurants'):
    self.send_response(code)
    self.send_header('Content-type', 'text/html')
    self.send_header('Location', location)
    self.end_headers()

  def _wrap_body_html(self, content):
    return "<html><body>" + content + "</body></html>"

  def _create_form(self):
    output = ""
    output += "<h1>Make a New Restaurant</h1>"
    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
    output += "<input name='new_restaurant_name' type='text' placeholder='New Restaurant Name' > "
    output += "<input type='submit' value='Create'>"
    output += "</form>"
    return output

  def _edit_form(self, restaurant):
    output = ""
    output += "<h1>" + restaurant.name + "</h1>"
    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurant.id
    output += "<input name='new_restaurant_name' type='text' placeholder='%s' >" % restaurant.name
    output += "<input type='submit' value='Rename'>"
    output += "</form>"
    return output

  def do_GET(self):
    try:
      if self.path.endswith("/restaurants/new"):
        self._send_text_header(200)
        content = self._wrap_body_html(self._create_form())
        self.wfile.write(content)

      if self.path.endswith("/restaurants"):
        restaurants = session.query(Restaurant).all()
        output = ""
        output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"

        self._send_text_header(200)
        for restaurant in restaurants:
          output += restaurant.name
          output += "</br>"
          output += "<a href ='#' >Edit </a> "
          output += "</br>"
          output += "<a href =' #'> Delete </a>"
          output += "</br>" * 3

        content = self._wrap_body_html(output)
        self.wfile.write(content)

      if re.search(r"/restaurants/\d+/edit", self.path):
        restaurant_id_path = self.path.split("/")[2]
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id_path).one()

        if restaurant:
          self._send_text_header(200)
          content = self._wrap_body_html(self._edit_form())
          self.wfile.write(content)

    except IOError:
      self.send_error(404, 'File Not Found: %s' % self.path)

  def do_POST(self):
    try:
      if re.search(r"/restaurants/\d+/edit", self.path):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

        if ctype == 'multipart/form-data':
          fields = cgi.parse_multipart(self.rfile, pdict)
          message_content = fields.get('new_restaurant_name')

          restaurant_id_path = self.path.split("/")[2]
          restaurant = session.query(Restaurant).filter_by(id=restaurant_id_path).one()

          if restaurant:
            restaurant.name = message_content[0]

            session.commit()
            session.add(restaurant)

            self._send_text_header_with_location(301)

      if self.path.endswith("/restaurants/new"):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

        if ctype == 'multipart/form-data':
          fields = cgi.parse_multipart(self.rfile, pdict)
          message_content = fields.get('new_restaurant_name')

          new_restaurant = Restaurant(name=message_content[0])
          session.add(new_restaurant)
          session.commit()

          self._send_text_header_with_location(301)

    except:
      pass

def main():
  try:
    server = HTTPServer(('', 8080), webServerHandler)
    print 'Web server running... Open localhost:8080/restaurants in your browser'
    server.serve_forever()
  except KeyboardInterrupt:
    print '^C received, shutting down server'
    server.socket.close()

if __name__ == '__main__':
  main()

