# Columbia Robotics Club
# MATE ROV Competition
# Lexis Sablan lrs2217@columbia.edu

# Uses opencv and tkinter GUI builder to display video feed from 3 cameras, 
# take a screenshot of a frame, and switch views using key binds


import numpy as np
import cv2
import tkinter as tk
import PIL
from PIL import Image, ImageTk
import time



# To run this program, open a new file and import this cams.py file and call the init function:
# cams.App(tk.Tk(), 'Camera Feed', 0, 1, 2)
# tk.Tk() creates a new winodw, 'Camera Feed' is a string for the title of the window, and 0, 1, 2 are the 
# locations of the video sources connected to the computer
class App:
	def __init__(self, window, window_title, video_source1, video_source2, video_source3):
		self.window = window
		self.window.configure(bg="black")
		self.window.title(window_title)
		# initializing the camera sources
		self.video_source1 = video_source1
		self.video_source2 = video_source2
		self.video_source3 = video_source3
		# these keep track of which key has been pressed in order to reorder the camera views
		self.a = 1
		self.s = 0
		self.d = 0
		# keeps track of how many screenshots have been taken
		self.screenshotCount = 1

		# separate class that handles opencv stuff
		self.vid1 = MyVideoCapture(self.video_source1, 1, 1, 640, 480)
		self.vid2 = MyVideoCapture(self.video_source2, 1, 1, 640, 480)
		self.vid3 = MyVideoCapture(self.video_source3, 1, 1, 640, 480)

		#create separate frame within window to hold all video canvases
		self.box = tk.Frame(window, bg="black")
		self.box.pack()

		# Binds the a, s, and d keys to reorder the views
		self.window.bind('a', lambda event: self.changeView(1, 0, 0))
		self.window.bind('s', lambda event: self.changeView(0, 1, 0))
		self.window.bind('d', lambda event: self.changeView(0, 0, 1))

		# creates 3 canvases with the first being the largest and the other two being smaller
		self.canvas1 = tk.Canvas(self.box, width = 1341, height = 1008, bg="black",  highlightthickness=0)
		self.canvas2 = tk.Canvas(self.box, width = 640, height = 480, bg="black",  highlightthickness=0)
		self.canvas3 = tk.Canvas(self.box, width = 640, height = 480, bg="black", highlightthickness=0)

		self.canvas1.grid(column=0, row = 0, rowspan = 2, columnspan = 2)
		self.canvas2.grid(column = 2, row = 0)
		self.canvas3.grid(column = 2, row = 1)

		# binds w key to take screenshot
		self.window.bind('w', lambda event: self.screenshot(0, 640, 480))

		# update window with new frames constantly
		self.delay = 15
		self.update()
		self.window.mainloop()


	# called with the a, s, d binds and updates these values to determine which view setting is pushed to screen
	def changeView(self, x, y, z):
		self.a = x
		self.s = y
		self.d = z


	# this function can only screenshot whichever video is in the first video capture slot. to be able to screenshot from any video feed, duplicate 
	# this function with appropriate video source index and create new key binds 

	def screenshot(self, video_source, resx, resy):
		cap = cv2.VideoCapture(video_source)
		cap.set(3, resx)
		cap.set(4, resy)
		if cap.isOpened():
		    ret, frame = cap.read()
		    if ret:
		    	# saves image to the current folder, add path if necessary to specify where to save
        		cv2.imwrite('screenshot'+str(self.screenshotCount)+'.png', frame)
        # increments screenshot count for file naming purposes
		self.screenshotCount+=1


	# this function constantly receives new frames from each feed and sends it to the 
	# appropriate canvas depending on the current view setting
	def update(self):
		# because this code is intended to work with one high res cam and two low res analog cams, we need to adjust the resolution
		# of the frames we send to each canvas when we reorder the views
		# these float values are hardcoded based off trial and error and what looks best with the current set up
		if self.a == 1:
			ret, frame1 = self.vid1.get_frame(2.1, 2.1)
			ret, frame2 = self.vid2.get_frame(1, 1)
			ret, frame3 = self.vid3.get_frame(1, 1)
		elif self.s == 1:
			ret, frame1 = self.vid1.get_frame(1,1)
			ret, frame2 = self.vid2.get_frame(2.1, 2.1)
			ret, frame3 = self.vid3.get_frame(1, 1)
		elif self.d == 1:
			ret, frame1 = self.vid1.get_frame(1, 1)
			ret, frame2 = self.vid2.get_frame(1, 1)
			ret, frame3 = self.vid3.get_frame(2.1, 2.1)


		if ret:
			self.photo1 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame1))
			self.photo2 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame2))
			self.photo3 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame3))
			if self.a == 1:
				self.canvas1.create_image(0,0, image = self.photo1, anchor=tk.NW)
				self.canvas2.create_image(0,0, image = self.photo2, anchor=tk.NW)
				self.canvas3.create_image(0,0, image = self.photo3, anchor=tk.NW)
			elif self.s == 1:
				self.canvas1.create_image(0,0, image = self.photo2, anchor=tk.NW)
				self.canvas2.create_image(0,0, image = self.photo1, anchor=tk.NW)
				self.canvas3.create_image(0,0, image = self.photo3, anchor=tk.NW)
			elif self.d == 1:
				self.canvas1.create_image(0, 0, image = self.photo3, anchor=tk.NW)
				self.canvas2.create_image(0, 0, image = self.photo2, anchor=tk.NW)
				self.canvas3.create_image(0,0, image = self.photo1, anchor=tk.NW)

		self.window.after(self.delay, self.update)

# this function handles opencv stuff such as setting a VideoCapture object for each camera and reading frames
class MyVideoCapture:
	def __init__(self, video_source, scalex, scaley, resx, resy):
		self.vid = cv2.VideoCapture(video_source)
		self.vid.set(3, resx)
		self.vid.set(4, resy)
		if not self.vid.isOpened():
			raise ValueError("Unable to open video source", video_source)



	def get_frame(self, scalex, scaley):
		if self.vid.isOpened():
			ret, frame = self.vid.read()
			smaller_frame = cv2.resize(frame, (0,0), fx=scalex, fy=scaley)
			if ret:
				return (ret, cv2.cvtColor(smaller_frame, cv2.COLOR_BGR2RGB))
			else: return (ret, none)
		else: 
			return (ret, none)



	def __del__(self):
		if self.vid.isOpened():
			self.vid.release()

App(tk.Tk(), 'Camera Feed', 0, 0, 0)
