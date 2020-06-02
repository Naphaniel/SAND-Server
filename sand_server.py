import socketserver
import threading
import socket
from sand_process import sand_process



class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        while True:

	        self.data = self.request.recv(1024).strip()
	        if not self.data:
	        	return

	        cur_thread = threading.current_thread()
	        
	        if self.data == '3G'.encode():
		        file_path = sand_process('3_G')
	        	self.request.sendall(file_path.encode())
	        if self.data == '3L'.encode():
		        file_path = sand_process('3_L')
	        	self.request.sendall(file_path.encode())
	        if self.data == '3GL'.encode():
		        file_path = sand_process('3_GL')
	        	self.request.sendall(file_path.encode())

	        if self.data == '10G'.encode():
		        file_path = sand_process('10_G')
	        	self.request.sendall(file_path.encode())
	        if self.data == '10L'.encode():
		        file_path = sand_process('10_L')
	        	self.request.sendall(file_path.encode())
	        if self.data == '10GL'.encode():
		        file_path = sand_process('10_GL')
	        	self.request.sendall(file_path.encode())

	        if self.data == '32G'.encode():
		        file_path = sand_process('32_G')
	        	self.request.sendall(file_path.encode())
	        if self.data == '32L'.encode():
		        file_path = sand_process('32_L')
	        	self.request.sendall(file_path.encode())
	        if self.data == '32GL'.encode():
		        file_path = sand_process('32_GL')
	        	self.request.sendall(file_path.encode())

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass



if __name__ == "__main__":
    HOST, PORT = "localhost", 65432

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    with server:
    	ip, port = server.server_address
    	server_thread = threading.Thread(target=server.serve_forever)
    	server_thread.daemon = True
    	server_thread.start()
    	print("Server open")
    	server.serve_forever()

