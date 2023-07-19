import socket
import threading
from math import *
from random import *

def blink(matrix, f):
	for i in range(100000):
		brightness = f(i)
		matrix.setColor([(0,0,brightness), "#000000"])
		for j in range(8):
			for k in range(8):
				matrix.set(j,k)


def twinkle(matrix, f, probability):
	for i in range(100000):
		brightness = f(i)
		matrix.setColor([(0,0,brightness), "#000000"])
		for j in range(8):
			for k in range(8):
				if random() < probability:
					matrix.set(j,k)

class Matrix:
	def __init__(self, size):
		self.matrix = [[ [(0x00,0x00,0x00),"#000000"] for i in range(size)] for j in range(size)] #an optimization is to keey this as a byte array
		self.color = [(0x05,0x05,0x05),"#050505"]
	
	def __len__(self):
		return len(self.matrix)
	
	def __getitem__(self,key):
		return self.matrix[key]
	
	def set(self, i, j):
		self.matrix[i][j] = self.color
	
	def set_position(self, x, y, window_size):
		row = y // (window_size//len(self.matrix))
		column = x // (window_size//len(self.matrix))
		
		if row >= len(self.matrix):
			row = len(self.matrix) - 1
		elif row < 0:
			row = 0
		
		if column >= len(self.matrix):
			column = len(self.matrix) - 1
		elif column < 0:
			column = 0
		
		self.set(row, column)
	
	def setColor(self,color): #must be a tuple pair or just make an object that can represent it =
		self.color = color
		
		
	def clear(self):
		for i in range(len(self.matrix)):
			for j in range(len(self.matrix[i])):
				self.matrix[i][j] = [(0x00,0x00,0x00),"#000000"]
	
	def getBytes(self):
		bytes = bytearray()
		mode= True
		for row in self.matrix:
			di = None
			i = None
			if mode:
				di = -1
				i = len(row) - 1
			else:
				di = 1
				i = 0
				
				
			while 0 <= i and i <= len(row) - 1:
				item = row[i]
				for rgb in item[0]:
					bytes.append(int(rgb))
				i += di
			mode = not mode
		
				
		return bytes


#'192.168.1.7'    8090
class Server:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.sock = socket.socket()
		self.connections = []
		self.running = True
	
	def run(self):
		self.sock.bind((self.ip,self.port))
		self.sock.listen(0)
	
	def handler(self):
		pass
	
	def stop(self):
		self.running = False
		for i in range(1000):
			pass
		self.sock.close()
		#print("closing")


class RGBMatrix(Matrix, Server):
	def __init__(self, size = 8, ip = '192.168.1.7', port = 8090):
		Server.__init__(self, ip, port)
		Matrix.__init__(self, size)
	
	def handler(self, c, a):
		while self.running:
			data = 0
			try:
				data = c.recv(1024)
				for connection in self.connections:
					#print(data)
					connection.send(self.getBytes())
			except:
				pass
			if not data:
				#print(str(a[0]),":", str(a[1]), "disconnected")
				self.connections.remove(c)
				c.close()
				break
				
	def start(self):
		thread = threading.Thread(target=self.run)
		thread.daemon = True
		thread.start()
		
	def run(self):
		Server.run(self)
		while self.running:
			c,a = self.sock.accept()
			thread = threading.Thread(target=self.handler, args=(c,a))
			thread.daemon = True
			thread.start()
			self.connections.append(c)
			#print(str(a[0]),":", str(a[1]), "connected")
		

"""
matrix = RGBMatrix(8, '192.168.1.7',  8090)

try:
	matrix.start()
	matrix.setColor([(5,0,0), "#050000"])
	while True:
		for i in range(8):
			for j in range(8):
				matrix.set(i,j)
				
except:
	matrix.stop()
"""
		



		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		