import tkinter as tk
from tkinter.colorchooser import *
import socket
import threading

SIZE = 500

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
	
	def setColor(self,color):
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
		
		print(len(bytes))
				
		return bytes
		
		

class View:
	def __init__(self, parent):
		parent.geometry("{:d}x{:d}".format(SIZE,SIZE + 70))
		self.canvas = tk.Canvas(parent, width=SIZE, height=SIZE)
		self.canvas.pack(expand=1, fill=tk.BOTH)
		self.button = tk.Button(parent, text="clear")
		self.button.pack()
		self.button2 = tk.Button(parent, text="color")
		self.button2.pack()
		self.size = SIZE
		self.parent = parent
	
	def draw(self, matrix):
		pixel_dimensions = self.size/len(matrix)
		self.canvas.delete("all")
		for i in range(len(matrix)):
			for j in range(len(matrix[0])):
				self.canvas.create_rectangle(j * pixel_dimensions, i * pixel_dimensions, j*pixel_dimensions + pixel_dimensions, i * pixel_dimensions + pixel_dimensions, fill=matrix[i][j][1])

class Server:
	def __init__(self):
		self.sock = socket.socket()
		self.connections = []
		self.sock.bind(('0.0.0.0', 8080 ))
		self.sock.listen(0)
		self.running = True
	
	def run(self):
		pass
	
	def handler(self):
		pass
	
	def stop(self):
		self.running = False
		for i in range(1000):
			pass
		self.sock.close()
		print("closing")

class Controller(Server):
	def __init__(self, view, model):
		super().__init__()
		view.parent.protocol("WM_DELETE_WINDOW", lambda:[self.stop(), view.parent.destroy()])
		view.canvas.bind("<B1-Motion>", self.response)
		view.button["command"] = self.clear
		view.button2["command"] = self.setColor
		self.view = view
		self.model = model
		self.view.draw(self.model)
		thread = threading.Thread(target=self.run)
		thread.daemon = True
		thread.start()
	
	
	def handler(self, c, a):
		while self.running:
			data = 0
			try:
				data = c.recv(1024)
				for connection in self.connections:
					print(data)
					connection.send(self.model.getBytes())
			except Exception as e:
				print(e)
			if not data:
				print(str(a[0]),":", str(a[1]), "disconnected")
				self.connections.remove(c)
				c.close()
				break
		
	def run(self):
		while self.running:
			c,a = self.sock.accept()
			thread = threading.Thread(target=self.handler, args=(c,a))
			thread.daemon = True
			thread.start()
			self.connections.append(c)
			print(str(a[0]),":", str(a[1]), "connected")
		
	
	def response(self, event):
		self.model.set_position(event.x, event.y, self.view.size)
		self.view.draw(self.model)
	
	def clear(self):
		self.model.clear()
		self.view.draw(self.model)
	
	def setColor(self):
		#print(self.model.getBytes())
		color = askcolor()
		#print(color)
		self.model.setColor(color)
		
#461 27  to 3 0
		

class Application:
	def __init__(self):
		window = tk.Tk()
		Controller(View(window), Matrix(8))
		window.mainloop()

def main():
	Application()
main()	