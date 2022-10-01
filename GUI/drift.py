# Columbia University Robotics Club
# MATE ROV Competition 2022
# Lexis Sablan lrs2217@columbia.edu

# Determines the location a ship has drifted to given the angle, speed, and time elapsed in hours

import math
import tkinter as tk 


class Drift_Calc:

	def __init__(self, container):
		self.container = container

		self.title = tk.Label(self.container, text='Drift Calculator')
		self.title.grid()

		self.input_box = tk.Entry(self.container, width=30)
		self.input_box.insert(0, 'Enter angle,speed,hours')
		self.input_box.grid()

		self.but = tk.Button(self.container, text='Calculate', command=self.drift)
		self.but.grid()

	def drift(self):
		self.input = self.input_box.get()


		self.values = self.input.split(",")
		self.angle = float(self.values[0])
		self.speed = float(self.values[1])
		self.hours = float(self.values[2])

		self.dist = round((self.hours*3600*self.speed)/1000, 2)

		self.opp = abs(round(math.sin(math.radians(self.angle))*self.dist, 2))
		self.adj = abs(round((math.sin(math.radians(180-90-self.angle)))*self.dist, 2))

		self.opp_squares = round(self.opp/2)
		self.adj_squares = round(self.adj/2)


		self.total_dist = tk.Label(self.container, text = str(self.dist) + ' km total')
		self.total_dist.grid()

		if(self.angle<90):
			self.vector1 = (str(self.opp) + ' East = ' + str(self.opp_squares) + ' squares East')
			self.vector2 = (str(self.adj) + ' North = ' + str(self.adj_squares) + ' squares North')
		elif(self.angle<180):
			self.vector1 = (str(self.opp) + ' East = ' + str(self.opp_squares) + ' squares East')
			self.vector2 = (str(self.adj) + ' South = ' + str(self.adj_squares) + ' squares South')
		elif(self.angle<270):
			self.vector1 = (str(self.opp) + ' West = ' + str(self.opp_squares) + ' squares West')
			self.vector2 = (str(self.adj) + ' South = ' + str(self.adj_squares) + ' squares South')
		else:
			self.vector1 = (str(self.opp) + ' West = ' + str(self.opp_squares) + ' squares West')
			self.vector2 = (str(self.adj) + ' North = ' + str(self.adj_squares) + ' squares North')

		self.vector1_result = tk.Label(self.container, text=self.vector1)
		self.vectro2_result = tk.Label(self.container, text = self.vector2)
		self.vector1_result.grid()
		self.vectro2_result.grid()



