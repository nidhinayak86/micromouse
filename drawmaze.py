from maze import Maze
import turtle
import sys
import random

class DrawMaze (object):


	def __init__(self, testmaze):
		'''
		This function uses Python's turtle library to draw a picture of the maze
		given as an argument when running the script.
		'''

		# Create a maze based on input argument on command line.
		#testmaze = Maze( str(sys.argv[1]) )

		# Intialize the window and drawing turtle.
		window = turtle.Screen()
		wally = turtle.Turtle()
		wally.speed(0)
		#wally.hideturtle()
		wally.penup()

		self.testmaze=testmaze

		self.textTurtle= turtle.Turtle()
		self.textTurtle.penup()
		self.textTurtle.goto(window.window_width()/-2 -10,window.window_height()/-2 +10)
		self.textTurtle.pendown()
		self.turtlecolor='black'
		# maze centered on (0,0), squares are 20 units in length.
		sq_size = 20
		self.mazeDim=testmaze.dim
		origin = testmaze.dim * sq_size /-2

		# iterate through squares one by one to decide where to draw walls
		for x in range(testmaze.dim):
			for y in range(testmaze.dim):
				if not testmaze.is_permissible([x,y], 'up'):
					wally.goto(origin + sq_size * x, origin + sq_size * (y+1))
					wally.setheading(0)
					wally.pendown()
					wally.forward(sq_size)
					wally.penup()

				if not testmaze.is_permissible([x,y], 'right'):
					wally.goto(origin + sq_size * (x+1), origin + sq_size * y)
					wally.setheading(90)
					wally.pendown()
					wally.forward(sq_size)
					wally.penup()

				# only check bottom wall if on lowest row
				if y == 0 and not testmaze.is_permissible([x,y], 'down'):
					wally.goto(origin + sq_size * x, origin)
					wally.setheading(0)
					wally.pendown()
					wally.forward(sq_size)
					wally.penup()

				# only check left wall if on leftmost column
				if x == 0 and not testmaze.is_permissible([x,y], 'left'):
					wally.goto(origin, origin + sq_size * y)
					wally.setheading(90)
					wally.pendown()
					wally.forward(sq_size)
					wally.penup()

		wally.setheading(90)
		wally.goto(origin + sq_size / 2, origin + sq_size / 2)
		self.wallyTurtle=wally

	def drawSearchPath(self, x, y , heading):
		print("printing line=" ,str(heading))
		# maze centered on (0,0), squares are 20 units in length.
		sq_size = 20
		origin = self.mazeDim * sq_size / -2 
		mytutle=self.wallyTurtle
		mytutle.speed(1)
		if x== 0 and y ==1 :
			newColor=random.choice(['red', 'green' ])
			if newColor != self.turtlecolor :
				mytutle.color(newColor)
				self.turtlecolor= newColor
			else:
				mytutle.color('blue')
				self.turtlecolor= 'blue'
				#fins another color
			mytutle.pensize(4)
		mytutle.pendown()

		if heading == 'u':
			mytutle.goto(origin + sq_size * x + sq_size / 2, origin + sq_size * (y) + sq_size / 2)
			
			#mytutle.forward(sq_size)
			mytutle.penup()

		elif heading == 'b' :
			mytutle.goto(origin + sq_size * x + sq_size / 2, origin + sq_size * (y) + sq_size / 2)
			
			#mytutle.backward(sq_size)
			mytutle.penup()

		else:
			pass
		"""
		mytutle.goto(origin + sq_size * x +sq_size/2 , origin + sq_size * (y+1)+sq_size/2)
		#mytutle.setheading(heading)
		mytutle.pendown()
		mytutle.forward(sq_size)
		mytutle.penup()
		"""




	def changeDirection(self,  rotationNext ,robotHeading ):
		print("changing heading=" ,str(rotationNext))
		# maze centered on (0,0), squares are 20 units in length.
		
		nextHeading=""
		if robotHeading == 'u':
			nextHeading =90
		elif robotHeading == 'd':
			nextHeading =270
		elif robotHeading == 'l':
			nextHeading =180
		else:
			nextHeading =0

		mytutle=self.wallyTurtle
		mytutle.pendown()
		if rotationNext ==90:
			mytutle.right(90)
			print("changed heading=" ,mytutle.heading())
			if(mytutle.heading() != int( nextHeading)) :
				print("error occured ")
				#mydata = raw_input('Prompt : verify rotation')
				mytutle.setheading(int( nextHeading))


		if rotationNext ==-90:
			mytutle.left(90)
			print("changed heading=" ,mytutle.heading())
			if(mytutle.heading() != int(nextHeading)) :
				print("error occured ")
				#mydata = raw_input('Prompt : verify rotation')
				mytutle.setheading(int( nextHeading))


		#mytutle.forward(sq_size/2)
		mytutle.penup()
		#pass

	def writeText(self, arg):
		self.textTurtle.undo()
		self.textTurtle.write(arg, move=False, align="left", font=("Arial", 8, "normal"))