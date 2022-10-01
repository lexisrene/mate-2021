import tkinter as tk


class Biomass_calc:
	def __init__(self, container):
		self.container = container

		self.title = tk.Label(self.container, text='Biomass Calculator')
		self.title.grid()
		# create entry bos to receive input from user
		self.input_box = tk.Entry(self.container, width=30)
		# user inputs numbers in specific format where n is the number of fish in the pen, l is the average lenght
		# and a and b are given by the judge
		self.input_box.insert(0, "Enter n,l,a,b")
		self.input_box.grid()

		# create a start button to calculate
		self.enter = tk.Button(self.container, text="Calculate", command=self.myClick)
		self.enter.grid()

	def myClick(self):
		# receive and hold the input
		input = self.input_box.get()
		# divide the string into the individual values
		values = input.split(",")
		n = float(values[0])
		l = float(values[1])
		a = float(values[2])
		b = float(values[3])
		# compute using formula in manual
		m = (n*a*(pow(l, b)))*pow(10, -3)

		# return the result in a label
		mass = tk.Label(self.container, text="Biomass: " + str(m))
		mass.grid()

