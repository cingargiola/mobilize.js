import SimpleHTTPServer
import SocketServer
import urllib
import Cookie

PORT = 8081

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	base = SimpleHTTPServer.SimpleHTTPRequestHandler
	def do_GET(self):
		#print "doGET", self.path
		
		if "cookie" in self.headers.dict:
			cookies = Cookie.SimpleCookie()
			cookies.load(self.headers.dict["cookie"])		
			if cookies["mobilize-mobile"].value == "1":
				print "Cookie says client is mobile"											
								
		if "/log" in self.path:
			msg = urllib.unquote(self.path.split("msg=")[-1])
			while msg.endswith("/"):
				msg = msg[:-1]
			print msg
			self.send_response(200)
			self.end_headers()
			return
		
		return self.base.do_GET(self)

	def log_request(self,code):
		if "/log" in self.path:
			return
		return self.base.log_request(self, code)

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
