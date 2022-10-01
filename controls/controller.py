# MATE ROV 2022 Competition

# Receives input from controller (currently configured for Xbox X controller) and translates the input into
# output values for 6 motors in vector drive

# Uses pygame to handle controller input, and sends the values for the motors in an array to the arduino serial

import pygame
from pygame import *
import numpy
import serial
from serial import Serial



class Controller:

	def __init__(self, ard_port):
		# setting up pygame stuff
		pygame.init()
		pygame.display.set_caption('ROV')
		pygame.joystick.init()
		self.screen = pygame.display.set_mode([30,30])
		self.clock = pygame.time.Clock()

		# setting up arduino object to send serial comms 
		self.ard_port = ard_port
		self.arduino = serial.Serial(port=self.ard_port, baudrate=115200, timeout=.1)

		self.done = False

		# mapping buttons for xbox x controller
		self.LEFT_HORI = 0
		self.RIGHT_HORI = 3
		self.LEFT_VERT = 1
		self.RIGHT_VERT = 4

		self.LEFT_BUMPER = 2
		self.RIGHT_BUMPER = 5

		self.LEFT_TRIGGER = 4
		self.RIGHT_TRIGGER = 5

		# default value for when motor is off
		self.STOP_VAL = "1500"
		self.cur_grip = '90'

		# initializing each of the motors
		self.reset()

		# array of values for the motor to be passed over to the arduinp
		self.motor_arr = [self.MOTOR1, self.MOTOR2, self.MOTOR3, self.MOTOR4, self.MOTOR5, self.MOTOR6, self.cur_grip]

	def move(self):
		while not self.done:
			self.screen.fill([0, 0, 0])

			# reset the motors to off-state when no input from controller
			self.reset()

			# exit pygame window to quit loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.done = True

			# initialize joystick
			joy = pygame.joystick.Joystick(0)
			joy.init()


			# set up axis responsible for up/down, fwd/bkwd, rotating, and strafing
			self.UD_axis = joy.get_axis(self.LEFT_VERT)
			self.FB_axis = joy.get_axis(self.RIGHT_VERT)
			self.rot = joy.get_axis(self.RIGHT_HORI)
			self.strafeL = joy.get_axis(self.LEFT_BUMPER)
			self.strafeR = joy.get_axis(self.RIGHT_BUMPER)
			self.strafe = -self.strafeL + self.strafeR

		
			self.grip_close = joy.get_button(self.RIGHT_TRIGGER)
			self.grip_open = joy.get_button(self.LEFT_TRIGGER)

			# send axis positions to be evaluated for motor values
			self.motor_vector(self.UD_axis, self.FB_axis, self.rot, self.strafe)

			self.servos(self.grip_close, self.grip_open)

			# sends values to the arduino 
			self.send_ard(self.motor_arr)



			print(self.motor_arr)

			self.clock.tick(60)



	def motor_vector(self, UP, FB, rot, strafe):
		# if the left vertical axis is activated, map the value and send the same value to the up/down motors
		if(UP > 0.1 or UP < -0.1):
			UD_val = int(numpy.interp(UP, [-1,1], [1100, 1900]))
			self.MOTOR1 = UD_val
			self.MOTOR2 = UD_val
			self.MOTOR3 = self.STOP_VAL
			self.MOTOR4 = self.STOP_VAL
			self.MOTOR5 = self.STOP_VAL
			self.MOTOR6 = self.STOP_VAL

		# if the right vert axis is activated, map the value and send the same value to all 4 horizontal motors
		if(FB > 0.1 or FB < -0.1):
			FB_val = int(numpy.interp(FB, [-1,1], [1100, 1900]))

			self.MOTOR1 = self.STOP_VAL
			self.MOTOR2 = self.STOP_VAL
			self.MOTOR3 = FB_val
			self.MOTOR4 = FB_val
			self.MOTOR5 = FB_val
			self.MOTOR6 = FB_val

		# for yaw axis in vector drive, motors diagonal from each other thrust in the same direction
		if(rot > 0.1 or rot < -0.1):
			# to rotate with the right horizontal joystick axis, get two values that are opposite in direction by reversing the mapping
			LR1_val = int(numpy.interp(rot, [-1,1], [1100, 1900]))
			LR2_val = int(numpy.interp(rot, [-1,1], [1900, 1100]))

			self.MOTOR1 = self.STOP_VAL
			self.MOTOR2 = self.STOP_VAL
			self.MOTOR3 = LR1_val
			self.MOTOR4 = LR2_val
			self.MOTOR5 = LR2_val
			self.MOTOR6 = LR1_val

			
		# for strafing, motors on the left thrust in the same direction while motors on the right thrust in the opposite direction
		if(strafe > 0.1 or strafe < -0.1):
			LR1_val = int(numpy.interp(strafe, [-1,1], [1100, 1900]))
			LR2_val = int(numpy.interp(strafe, [-1,1], [1900, 1100]))

			self.MOTOR1 = self.STOP_VAL
			self.MOTOR2 = self.STOP_VAL
			self.MOTOR3 = LR1_val
			self.MOTOR4 = LR2_val
			self.MOTOR5 = LR1_val
			self.MOTOR6 = LR2_val

		# continuously updates the motor values in the array
		self.motor_arr = [self.MOTOR1, self.MOTOR2, self.MOTOR3, self.MOTOR4, self.MOTOR5, self.MOTOR6, self.cur_grip.rjust(3, '0')]

	def servos(self, grip_open, grip_close):
		if(grip_close == 1):
			self.cur_grip = '00'
		if(grip_open == 1):
			self.cur_grip = '180'



		self.motor_arr = [self.MOTOR1, self.MOTOR2, self.MOTOR3, self.MOTOR4, self.MOTOR5, self.MOTOR6, self.cur_grip.rjust(3, '0')]




	def send_ard(self, values):
		# converts motor value array to string to send to arduino
		values = " ".join(str(x) for x in values)
		self.arduino.write(bytes(values, 'utf-8'))

	def reset(self):
		#sets the motors to off position
		self.MOTOR1 = self.STOP_VAL
		self.MOTOR2 = self.STOP_VAL
		self.MOTOR3 = self.STOP_VAL
		self.MOTOR4 = self.STOP_VAL
		self.MOTOR5 = self.STOP_VAL
		self.MOTOR6 = self.STOP_VAL


controller = Controller('/dev/cu.usbmodem1101')
controller.move()
