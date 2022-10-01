import tkinter as tk
import PIL
from PIL import Image, ImageTk
from tkinter import filedialog as fd

class Measure_Length: 
	def __init__(self, container, directory, known_length):
		self.directory = directory
		self.known_length = known_length
		self.container = container
		self.click_count = 0
		self.ref_pix = 0

		self.choose_img()
		self.reference()
		


	def choose_img(self):
		self.click_count = 0
		self.img_file = fd.askopenfilenames(initialdir =  self.directory, title = "Select Image")
		self.img = Image.open(self.img_file[0])
		self.img = self.img.resize((640, 480), Image.ANTIALIAS)
		self.img = ImageTk.PhotoImage(self.img)	

		self.container.create_image(130, 30, anchor = tk.NW, image = self.img)

		self.replace_but = tk.Button(text='Replace Image', command = self.choose_img)
		self.container.create_window(800, 250, anchor=tk.NW, window=self.replace_but)

	def reference(self):
		self.container.bind('<Button-1>', lambda event: self.calc_reference(event, 'red', 2))
		
	def calc_reference(self, event, color, size):
		self.click_count+=1
		if self.click_count == 1:
			self.dot1x=event.x
			self.dot1y=event.y
			self.container.create_oval(self.dot1x,self.dot1y,self.dot1x+6,self.dot1y+6, fill=color, width=size)
		else:
			self.dot2x=event.x
			self.dot2y=event.y
			self.container.create_oval(self.dot2x,self.dot2y,self.dot2x+6,self.dot2y+6, fill=color, width=size)
			self.container.create_line(self.dot1x, self.dot1y, self.dot2x, self.dot2y, fill=color, width = 4)
			self.ref_pix = self.known_length / (abs(self.dot2x - self.dot1x)) 
			self.ref_label = tk.Label(self.container, text ="1 pixel = " + str(round(self.ref_pix, 3)) + " centimeters", )
			self.container.create_window(800, 300, anchor=tk.NW, window= self.ref_label)
			self.click_count = 3
			return

	def length(self):
		self.click_count = 0
		self.container.bind('<Button-1>', lambda event: self.calc_length(event, 'black', 2))

	def calc_length(self, event, color, size):
		self.click_count+=1
		if self.click_count % 2 != 0:
			self.dot1x=event.x
			self.dot1y=event.y
			self.container.create_oval(self.dot1x,self.dot1y,self.dot1x+6,self.dot1y+6, fill=color, width=size)
		else:
			self.dot2x=event.x
			self.dot2y=event.y
			self.container.create_oval(self.dot2x,self.dot2y,self.dot2x+6,self.dot2y+6, fill=color, width=size)
			self.container.create_line(self.dot1x, self.dot1y, self.dot2x, self.dot2y, fill=color, width = 4)
			self.length = (abs(self.dot2y - self.dot1y)) * self.ref_pix
			self.len_label = tk.Label(self.container, text ="Length = " + str(round(self.length, 3)))
			self.container.create_window(800, 320, anchor=tk.NW, window= self.len_label)
			self.click_count = 0
			return
		
		