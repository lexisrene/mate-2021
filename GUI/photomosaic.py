import cv2
import numpy as np 
import tkinter as tk 
import PIL
from PIL import Image, ImageTk
import corner

class Photomosaic:
	def __init__(self, canvas, img_files):
		self.canvas = canvas
		self.img_files = img_files
		self.img_list = []
		for i in range(0,8):
			self.img_list.append(self.display_pm(self.img_files[i]))
			
		self.canvas.create_image(50, 100, anchor = tk.NW, image = self.img_list[0])
		self.canvas.create_image(270, 100, anchor = tk.NW, image = self.img_list[3])
		self.canvas.create_image(490, 100, anchor = tk.NW, image = self.img_list[4])
		self.canvas.create_image(700, 100, anchor = tk.NW, image = self.img_list[7])
		self.canvas.create_image(50, 300, anchor = tk.NW, image = self.img_list[1])
		self.canvas.create_image(270, 300, anchor = tk.NW, image = self.img_list[2])
		self.canvas.create_image(490, 300, anchor = tk.NW, image = self.img_list[5])
		self.canvas.create_image(700, 300, anchor = tk.NW, image = self.img_list[6])

		self.pm_but = tk.Button(text='Create Photomosiac', command = self.stitch)
		self.canvas.create_window(440, 500, anchor=tk.NW, window=self.pm_but)

	def display_pm(self, img_file):
		self.img_file = img_file
		self.img = Image.open(self.img_file)
		self.img = self.img.resize((213, 160), Image.ANTIALIAS)
		self.img = ImageTk.PhotoImage(self.img)
		return self.img

	def stitch(self):
		self.canvas.delete('all')
		self.count = 1
		self.cropped = []
		self.crop_list = []
		for img in self.img_files:
			self.crop = corner.Crop_Rect(img)
			cv2.imwrite('rect' + str(self.count) + '.jpg', self.crop.get_cropped())
			self.cropped.append('rect' + str(self.count) + '.jpg')
			self.count+=1

		self.canvas.delete('all')
		for img in self.cropped:
			self.crop_list.append(self.display_pm(img))

		self.canvas.create_image(50, 100, anchor = tk.NW, image = self.crop_list[0])
		self.canvas.create_image(258, 100, anchor = tk.NW, image = self.crop_list[3])
		self.canvas.create_image(466, 100, anchor = tk.NW, image = self.crop_list[4])
		self.canvas.create_image(677, 100, anchor = tk.NW, image = self.crop_list[7])
		self.canvas.create_image(50, 255, anchor = tk.NW, image = self.crop_list[1])
		self.canvas.create_image(258, 255, anchor = tk.NW, image = self.crop_list[2])
		self.canvas.create_image(466, 255, anchor = tk.NW, image = self.crop_list[5])
		self.canvas.create_image(677, 255, anchor = tk.NW, image = self.crop_list[6])
		

