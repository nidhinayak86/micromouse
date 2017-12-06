"""###################################################
	FLOOD FILL ALGORITHM BY NIDHI UDACITY
####################################################"""
from maze import Maze
import random
import turtle
import sys
import pdb
import numpy as np
import queue
from pathOptimisation import pathOptimizer

	
class Stack:
	def __init__(self):
		self.items = []

	def isEmpty(self):
		return self.items == []

	def push(self, item):
		self.items.append(item)

	def pop(self):
		return self.items.pop()

	def peek(self):
		return self.items[len(self.items)-1]

	def size(self):
		return len(self.items)

	def printst(self):
		print((self.items))


class floodFill(object):
	def __init__(self, location, heading, goal_bounds, mazeDim , exploringAfterGoalReached=False):
		print("############################BEGIN FLood fill #############################")

		global stackNext 
		stackNext = Stack()
		global mazeWalls 
		global PosR 
		global PosC, direction  #This is needed to change the value of these variables
		global GoalR , GoalC ,mazeDepth ,mazeDimension ,scanDepth 
		global pathOptimizerObj
		global exploreAfterGoalReached 
		exploreAfterGoalReached= exploringAfterGoalReached
		pathOptimizerObj= pathOptimizer()
		#Assuming maze is 16x16... Robot starts in south west corner.
		#Cell 0,0 (Rows, Columns) is in the Northwest corner.
		#global oldLocation 
		self.oldLocation =[0,0]
		# 0...15
		# :
		# 15
		 
		self.isGoalReached= False
		self.previousTrip= False

		mazeDimension = mazeDim
		self.mazeDim=mazeDim
		#Initial position and direction
		PosR = location[0] #Row position
		PosC = location[1] #Column position
		direction = heading #robots rotation (heading) N, E, S, W
		
		#The goal "cell" (I just used one of the four goal cells).
		GoalR = goal_bounds[0]
		GoalC = goal_bounds[0]
		 
		#Initializing the mazeWalls 3-D Array 16x16x4 (booleans essentially)
		mazeWalls = [0]*mazeDim #maze wall storage NESW
		for j in range(0,mazeDim): #one way of creating nested list
			mazeWalls[j] = [0]*mazeDim
			for k in range(0,mazeDim): 
				mazeWalls[j][k] = [0]*4
		 

		global mazeDepth
		#Initializing the depth array 16x16 signed int
		mazeDepth = [0]*mazeDim #another way of creating nested list (more efficient)
		for i, item in enumerate(mazeDepth): 
			mazeDepth[i] = [0]*mazeDim

		 
		#"zero" out depth (Negative one is an unscanned cell)
		for i, index in enumerate(mazeDepth):
			for j, item in enumerate(mazeDepth[i]):
				mazeDepth[i][j] = -1
	 
		  
		mazeDepth[PosR][PosC] = scanDepth = -1 #initialize scan depth and set robot position cell to zero.
		#Iterate (scan) through maze once for each depth to flood. (Robot is at depth 0)

		global q
		q = queue.LifoQueue()
		q.put([0,0,-1])

		self.finalPath=None
		self.testingPhase= False


	def reset(self):
		global q
		q = queue.LifoQueue()
		self.oldLocation =[0,0]
		self.previousTrip=False
		#global direction
		#irection='N'
		self.finalPath=self.findPathTestRun()
		self.testingPhase= True
			 
	def headingToDirection(self,heading):
		dir_heading = {'u': 'N', 'up': 'N','r': 'E','right': 'E', 'd': 'S','down': 'S' , 'l': 'W' , 'left':'W' } 
		return dir_heading[heading]
	

	def headingToRotation(self,direction):
		dir_heading = {'f': 0, 'forward': 0,'r': 90,'right': 90,'l': -90 , 'left':-90 } 
		return dir_heading[direction]

	def updateWalls(self ,sensing,oldLocation , oldHeading ):

		# global dictionaries for robot movement and sensing
		dir_sensors = {'u': ['l', 'u', 'r'], 'r': ['u', 'r', 'd'],
					   'd': ['r', 'd', 'l'], 'l': ['d', 'l', 'u'],
					   'up': ['l', 'u', 'r'], 'right': ['u', 'r', 'd'],
					   'down': ['r', 'd', 'l'], 'left': ['d', 'l', 'u']}
		dir_move = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0],
					'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]}
		dir_reverse = {'u': 'd', 'r': 'l', 'd': 'u', 'l': 'r',
					   'up': 'd', 'right': 'l', 'down': 'u', 'left': 'r'}
		
		print((sensing,oldLocation , oldHeading ))
		curr_cell=[None, None]     
		leftsensing=sensing[0]
		curr_cell[0]=oldLocation[0]
		curr_cell[1]=oldLocation[1]
		curr_left_direction=dir_sensors[oldHeading][0]
		curr_opp_left_direction=self.headingToDirection(curr_left_direction)
		while leftsensing>0:
			leftsensing =leftsensing- 1
			self.cellSetWall(curr_cell[0],curr_cell[1],curr_opp_left_direction)
			#print("mazeWalls["+str(curr_cell[0])+"]["+str(curr_cell[1])+"]: "+str(mazeWalls[curr_cell[0]][curr_cell[1]]))
			curr_cell[0] += dir_move[curr_left_direction][0]
			curr_cell[1] += dir_move[curr_left_direction][1]
			


		straightsensing=sensing[1]
		curr_cell[0]=oldLocation[0]
		curr_cell[1]=oldLocation[1]
		curr_straight_direction=dir_sensors[oldHeading][1]
		curr_opp_straight_direction=self.headingToDirection(curr_straight_direction)
		while straightsensing>0:
			straightsensing =straightsensing- 1
			self.cellSetWall(curr_cell[0],curr_cell[1],curr_opp_straight_direction)
			#print("mazeWalls["+str(curr_cell[0])+"]["+str(curr_cell[1])+"]: "+str(mazeWalls[curr_cell[0]][curr_cell[1]]))
			curr_cell[0] += dir_move[curr_straight_direction][0]
			curr_cell[1] += dir_move[curr_straight_direction][1]
			

		rightsensing=sensing[2]
		curr_cell[0]=oldLocation[0]
		curr_cell[1]=oldLocation[1]
		curr_right_direction=dir_sensors[oldHeading][2]
		curr_opp_right_direction=self.headingToDirection(curr_right_direction)
		while rightsensing>0:
			self.cellSetWall(curr_cell[0],curr_cell[1],curr_opp_right_direction)
			#print("mazeWalls["+str(curr_cell[0])+"]["+str(curr_cell[1])+"]: "+str(mazeWalls[curr_cell[0]][curr_cell[1]]))
			rightsensing =rightsensing- 1
			curr_cell[0] += dir_move[curr_right_direction][0]
			curr_cell[1] += dir_move[curr_right_direction][1]
		
	def printMaze(self):
		#PRINT THE MAZE AFTER FLOOD 
		#pdb.set_trace()                
		for j in range(len(mazeDepth)-1, -1,-1):
			for i in range(0,len(mazeDepth), 1):
				if mazeDepth[i][j] >-1 and  mazeDepth[i][j] <10:
					print(" "+str(mazeDepth[i][j]), end='  ')
				else:
					print(str(mazeDepth[i][j]), end='  ')
			print()
	# This function is called by the simulator to get the
	# next step the mouse should take.
	def nextStep(self ,sensing ,location,heading, oldLocation , oldHeading ):
		print(sensing)
		if self.testingPhase == True:
			return self.nextStepTesting(sensing ,location,heading, oldLocation , oldHeading )
		else:
			return self.nextStepExploration(sensing ,location,heading, oldLocation , oldHeading )
	
	def nextStepTesting(self ,sensing ,location,heading, oldLocation , oldHeading):

		print("############################# NEXT STEP Testing ##################################")
		print("previous location:" ,self.oldLocation)
		print("currentCell: "+str(location))
		global PosR ,PosC
		PosR = location[1] #Row position
		PosC = location[0] #Column position
		direction = self.headingToDirection(heading) #robots  (heading) to N, E, S, W
		#self.recordWalls()
		
		if((location[0] == int(self.oldLocation[0]) )and (location[1] == int(self.oldLocation[1]) )):
			#nextCell = next(self.modFloodfill())
			print(self.finalPath.queue)
			nextCell = self.finalPath.get()
			self.previousTrip=False
			self.oldLocation=nextCell
			return self.takeAction(nextCell, direction)
		else:
			print("error")
			nextCell =[self.oldLocation[0],self.oldLocation[1]]
			return self.takeAction(nextCell, direction)
			#return -1


	def nextStepExploration(self ,sensing ,location,heading, oldLocation , oldHeading ):
		print("############################# NEXT STEP Exploration ##################################")
		print("previous location:" ,self.oldLocation)
		print("currentCell: "+str(location))
		global PosR ,PosC
		global  exploreAfterGoalReached

		PosR = location[1] #Row position
		PosC = location[0] #Column position
		
		self.updateWalls(sensing,location , heading)
		direction = self.headingToDirection(heading) #robots  (heading) to N, E, S, W
		#self.recordWalls()
			
		if(self.isGoalReached==False and (location[0] == int(self.oldLocation[0]) )and (location[1] == int(self.oldLocation[1]) )):
			#nextCell = next(self.modFloodfill())
			nextCell = self.modFloodfill()
			self.previousTrip=False
			#pdb.set_trace()
			#if you have flooded enough to reach the goal position. STOP FLOODING!
			if self.ifreachedGoal(location)== True:
				self.isGoalReached= True 
				print("goal  is reached")
				
				#return  self.takeAction(nextCell, direction)
		elif(self.isGoalReached==True and  (location[0] == int(self.oldLocation[0]) )and (location[1] == int(self.oldLocation[1]))):
			if exploreAfterGoalReached and not q.empty():
				nextCell =self.modFloodfill()
				self.previousTrip=False
				if nextCell == []:
					self.reset()
					return  ('Reset', 'Reset')
			else:
				nextCell = []
				#empty queue to complete calculations
				while(not q.empty()):
					self.modFloodfill()
				self.previousTrip=False
				self.reset()
				#pdb.set_trace()
				return  ('Reset', 'Reset')
		else:
			self.previousTrip=True
			# robot was not able to reach previous goal
			#find path to last step action from current robot position
			print("# robot was not able to reach previous goal ")
			print("#find path to last step action from current robot position")
			#nextCell = q.get()
			pathList=self.findPathWhenStuck(location,self.oldLocation)
			print(pathList)
			#pdb.set_trace()
			#if(pathList ==None):
				#pdb.set_trace()
			nextCell = pathList[1]


		self.printMaze()
		#Debug prints
		print("nextCell: "+str(nextCell))
		print("Current Direction: "+str(direction))
		print("mazeWalls["+str(PosC)+"]["+str(PosR)+"]: "+str(mazeWalls[PosC][PosR]))
		
		# once exploreation  done find path
		#nextCell = self.findPath(nextCell)

		#stackNext.printst()
		if self.previousTrip==False :
			self.oldLocation=nextCell

		return self.takeAction(nextCell, direction)

	def takeAction(self,nextCell, direction):
		#print(nextCell, direction)

		global PosR ,PosC
		#print(PosC, PosR)
		if(nextCell == [-1,-1]):
			print("Cannot find path")
			return "Left"
		elif nextCell[1] < PosR: #if next cell is South of robot. 
			#based on the direction of the robot we need to move forward or turn.
			if(direction == "S"): 
				if(PosR -1 == nextCell[1]):
					PosR = nextCell[1]
					return (self.headingToRotation("forward") ,1)
				elif(PosR -2 == nextCell[1]):
					PosR = nextCell[1]
					return (self.headingToRotation("forward") ,2)
				elif(PosR -3 == nextCell[1]):
					PosR = nextCell[1]
					return (self.headingToRotation("forward") ,3)
				else:
					return (self.headingToRotation("forward") ,1)
			if(direction == "E"): 
				direction = "S"
				return (self.headingToRotation("right") ,1)
			if(direction == "N"): 
				direction = "E"
				return (self.headingToRotation("right") ,0)
			if(direction == "W"):
				direction = "S"
				return (self.headingToRotation("left") ,1)
		elif nextCell[0] > PosC: #if next cell is east of robot. 
			#based on the direction of the robot we need to move forward or turn.
			if(direction == "N"):
				direction = "E"
				return (self.headingToRotation("right") ,1)
			if(direction == "E"): 
				if(PosC +1 == nextCell[0]):
					PosC = nextCell[0]
					return (self.headingToRotation("forward") ,1)
				elif(PosC +2 == nextCell[0]):
					PosC = nextCell[0]
					return (self.headingToRotation("forward") ,2)
				elif(PosC +3 == nextCell[0]):
					PosC = nextCell[0]
					return (self.headingToRotation("forward") ,3)
				else:
					return (self.headingToRotation("forward") ,1)
				
			if(direction == "S"): 
				direction = "E"
				return (self.headingToRotation("left") ,1)
			if(direction == "W"):
				direction = "N"
				return (self.headingToRotation("right") ,0)
		elif nextCell[1] > PosR: #if next cell is North of robot. 
			#based on the direction of the robot we need to move forward or turn.
			if(direction == "N"): 
				direction = "N"
				if(PosR +1 == nextCell[1]):
					PosR = nextCell[1]
					return (self.headingToRotation("forward") ,1)
				elif(PosR +2 == nextCell[1]):
					PosR = nextCell[1]
					return (self.headingToRotation("forward") ,2)
				elif(PosR +3 == nextCell[1]):
					PosR = nextCell[1]
					return (self.headingToRotation("forward") ,3)
				else:
					return (self.headingToRotation("forward") ,1)
			if(direction == "E"): 
				direction = "N"
				return (self.headingToRotation("left") ,1)
			if(direction == "S"): 
				direction = "E"
				return (self.headingToRotation("left") ,0)
			if(direction == "W"):
				direction = "N"
				return (self.headingToRotation("right") ,1)
		elif nextCell[0] < PosC: #if next cell is west of robot. 
			#based on the direction of the robot we need to move forward or turn.
			if(direction == "N"):
				direction = "W"
				return (self.headingToRotation("left") ,1)
			if(direction == "E"): 
				direction = "N"
				return (self.headingToRotation("left") ,0)
			if(direction == "S"): 
				direction = "W"
				return (self.headingToRotation("right") ,1)
			if(direction == "W"):
				if(PosC -1 == nextCell[0]):
					PosC = nextCell[0]
					#pdb.set_trace()
					return (self.headingToRotation("forward") ,1)
				elif(PosC -2 == nextCell[0]):
					PosC = nextCell[0]
					return (self.headingToRotation("forward") ,2)
				elif(PosC -3 == nextCell[0]):
					PosC = nextCell[0]
					return (self.headingToRotation("forward") ,3)
				else:
					return (self.headingToRotation("forward") ,1)

		else:
			print("same location.")
			return (self.headingToRotation("forward") ,0)
	 
		 
	def modFloodfill(self):
		#scanDepth =mazeDepth[currCellX][currCellY]
		nextCell=[]
		
		global q
		global mazeDepth

		while(not q.empty()): #(255 is the overflow)
			print("queue is not empty")
			print(q.queue)
			item=q.get()
			curr_x=item[0]
			curr_y=item[1]
			if(mazeDepth[curr_x][curr_y]==-1 ):
				scanDepth =item[2]
				scanDepth += 1
			else:
				scanDepth =min(mazeDepth[curr_x][curr_y],item[2]+1)
			

			minDepthAtItem=self.getminDepthofAllneighbours(item[0],item[1])
			print(item)
			print("minDepthAtItem=",minDepthAtItem)
			print("mazeDepthAtItem=",mazeDepth[curr_x][curr_y])
			print("scanDepth=",scanDepth)
			if  minDepthAtItem+1 < mazeDepth[curr_x][curr_y] and (mazeDepth[curr_x][curr_y]!=-1 ) :
				print("step1")
				mazeDepth[curr_x][curr_y]=minDepthAtItem+1
				q.put([item[0],item[1],minDepthAtItem])
				currNodeneighbours=self.getExploredNeighbours(item[0],item[1])
				for nodes in currNodeneighbours:
					q.put([nodes[0],nodes[1],minDepthAtItem+1])

			elif minDepthAtItem+1 < scanDepth and (mazeDepth[curr_x][curr_y]==-1 ) :
				print("step2")
				mazeDepth[curr_x][curr_y]=minDepthAtItem+1
				q.put([item[0],item[1],minDepthAtItem])
				currNodeneighbours=self.getExploredNeighbours(item[0],item[1])
				stackNext.push([item[0],item[1],minDepthAtItem ])
				nextCell=[]
				for nodes in currNodeneighbours:
					q.put([nodes[0],nodes[1],minDepthAtItem+1])

			elif minDepthAtItem+1 >= scanDepth and (mazeDepth[curr_x][curr_y]==-1 ) :
				print("step3")
				
				mazeDepth[curr_x][curr_y]=minDepthAtItem+1
				currNodeneighbours=self.getUnExploredNeighbours(item[0],item[1])
				stackNext.push([item[0],item[1],minDepthAtItem ])
				nextCell=[curr_x,curr_y]
				#q.put([item[0],item[1],minDepthAtItem])
				for nodes in currNodeneighbours:
					q.put([nodes[0],nodes[1],minDepthAtItem+1])

				q.put([item[0],item[1],minDepthAtItem+1])
			else:
				print("step4")
				#continue
				currNodeneighbours=self.getUnExploredNeighbours(item[0],item[1])
				for nodes in currNodeneighbours:
					nextCell=[nodes[0],nodes[1]]
					q.put([nodes[0],nodes[1],mazeDepth[curr_x][curr_y]])

			

			if nextCell != []:
				print(q.queue)
				return nextCell 
			else:
				print("nextcell is empty")
				continue
		
			  
		
		print("no unexplored cells  left")
		return nextCell

	def ifreachedGoal(self, robot_pos):
		# check for goal entered
		goal_bounds = [self.mazeDim/2 - 1, self.mazeDim/2]
		if robot_pos[0] in goal_bounds and robot_pos[1] in goal_bounds:
			return True
		else:
			return False


#this function finds the explored neghbour of given x,y coordinate in maze
# no explore neighbour then emptylist
	def getExploredNeighbours(self,curr_x,curr_y):
		global mazeWalls
		global mazeDepth
		out_put=[]
		for x in range(curr_x-1,curr_x+2):
			for y in range(curr_y-1,curr_y+2):

				if (x==curr_x+1 and y==curr_y+1) or(x==curr_x-1 and y==curr_y-1) or (x==curr_x+1 and y==curr_y-1)or (x==curr_x-1 and y==curr_y+1) or (x==curr_x and y==curr_y):
					continue

				if (x >=0 and x < mazeDimension) and (y >=0 and y < mazeDimension) and (mazeDepth[x][y] != -1) : #if cell hasn't been labeled (-1)
					if ((x==curr_x-1 and y==curr_y) and mazeWalls[curr_x][curr_y][3] == 1 and mazeWalls[x][y][1]== 1 ):
						out_put=out_put+[[x,y ,mazeDepth[x][y]]]
						

					if ((x==curr_x+1 and y==curr_y) and mazeWalls[curr_x][curr_y][1] == 1 and mazeWalls[x][y][3]== 1):
						out_put=out_put+[[x,y ,mazeDepth[x][y]]]
						#yield nextCell

					if ((x==curr_x and y==curr_y-1) and mazeWalls[curr_x][curr_y][2] == 1 and mazeWalls[x][y][0]== 1):
						out_put=out_put+[[x,y ,mazeDepth[x][y]]]

					if ((x==curr_x and y==curr_y+1) and mazeWalls[curr_x][curr_y][0] == 1 and mazeWalls[x][y][2] == 1 ):
						out_put=out_put+[[x,y ,mazeDepth[x][y]]]
		
		print("explored neighbours of =",curr_x," ",curr_y)
		print(out_put)

		return out_put


#this function finds the new unexplored neghbour of given x,y coordinate in maze
# new member will be from n, e, s, w direction and also unexplored
	def getUnExploredNeighbours(self,curr_x,curr_y):

		global mazeWalls
		global mazeDepth
		out_put=[]
		for x in range(curr_x-1,curr_x+2):
			for y in range(curr_y-1,curr_y+2):

				if (x==curr_x+1 and y==curr_y+1) or(x==curr_x-1 and y==curr_y-1) or (x==curr_x+1 and y==curr_y-1)or (x==curr_x-1 and y==curr_y+1) or (x==curr_x and y==curr_y):
					continue


				if (x >=0 and x < mazeDimension) and (y >=0 and y < mazeDimension) and (mazeDepth[x][y] == -1) : #if cell hasn't been labeled (-1)


					if ((x==curr_x-1 and y==curr_y) and mazeWalls[curr_x][curr_y][3] == 1 and mazeWalls[x][y][1]== 1 ):
						out_put=out_put+[[x,y ,mazeDepth[x][y]]]
						

					if ((x==curr_x+1 and y==curr_y) and mazeWalls[curr_x][curr_y][1] == 1 and mazeWalls[x][y][3]== 1):
						out_put=out_put+[[x,y ,mazeDepth[x][y]]]
						
						#yield nextCell

					if ((x==curr_x and y==curr_y-1) and mazeWalls[curr_x][curr_y][2] == 1 and mazeWalls[x][y][0]== 1):
						out_put=out_put+[[x,y ,mazeDepth[x][y]]]
						print("test neighbour of =",curr_x," ",curr_y)
						print(out_put)

					if ((x==curr_x and y==curr_y+1) and mazeWalls[curr_x][curr_y][0] == 1 and mazeWalls[x][y][2] == 1 ):
						out_put=out_put+[[x,y ,mazeDepth[x][y]]]
		
		print("unexplored neighbours of =",curr_x," ",curr_y)
		print(out_put)
		return out_put

#getminDeptofAllneighbours

	def getminDepthofAllneighbours(self,curr_x,curr_y):

		global mazeWalls
		global mazeDepth
		if curr_x==0  and curr_y==0:
			return mazeDepth[0][0]

		neighbours=self.getExploredNeighbours(curr_x,curr_y)
		print("getminDepthofAllneighbours")
		mazeDepthList=[]
		for currNode in neighbours:
			print(currNode)
			mazeDepthList=mazeDepthList+[mazeDepth[currNode[0]][currNode[1]]]

		mazeDepthList.sort()
		print(mazeDepthList)
		return mazeDepthList[0]




	def findPathWhenStuck(self, sourceCell , targetCell): 
		#Starting at the goal, find the shortest path back to the robot.
		x = sourceCell[0] #These r and c are the coordinates of the cell being observed. (starting at the goal cell)
		y = sourceCell[1]
		scanDepth = mazeDepth[x][y] #this is the depth to the observed cell.
		qtmp = queue.Queue()
		qtmp.put([x,y,scanDepth,[]])
		
		markedSet= set()
		markedSet.add((x,y))

		setofSerchedNodes = [0]*self.mazeDim #maze wall storage NESW
		for j in range(0,self.mazeDim): #one way of creating nested list
			setofSerchedNodes[j] = [0]*self.mazeDim

		setofSerchedNodes[x][y]=1

		while(not qtmp.empty()): 
			scanDepth=scanDepth+1
			node=qtmp.get()
			neighbours=self.getExploredNeighbours(node[0],node[1])
			neighbours=neighbours+self.getUnExploredNeighbours(node[0],node[1])
			for currNode in neighbours:
				if(currNode[0]==targetCell[0] and currNode[1]==targetCell[1]):
					
					return node[3]+[[node[0],node[1]] ,[currNode[0],currNode[1]]]
				else:
				#add to queue to serch using breadfirst serach
					if(setofSerchedNodes[currNode[0]][currNode[1]]!=1):
						setofSerchedNodes[currNode[0]][currNode[1]]=1
						qtmp.put([currNode[0],currNode[1],scanDepth,node[3]+[[node[0],node[1]]] ]  )


		return None
	

	def findPathTestRun(self): 
		#Starting at the goal, find the shortest path back to the robot.
		r=int(self.mazeDim/2) - 1
		c=int(self.mazeDim/2)
		scanDepth = mazeDepth[r][c] #this is the depth to the observed cell.
		 # check for goal entered
		goal_bounds = [int(self.mazeDim/2) - 1, int(self.mazeDim/2)]
		for x in goal_bounds:
			for y in goal_bounds:
				if mazeDepth[x][y] != -1 :
					scanDepth = mazeDepth[x][y]
					r = x #These r and c are the coordinates of the cell being observed. (starting at the goal cell)
					c = y
					break

		print(scanDepth)
		qtmp = queue.LifoQueue()

		while(scanDepth > 0):
			print(qtmp)
			#If a cell with one less depth is next to the observed cell (with no walls separating) Then OBSERVE THAT CELL NEXT!
			#If that cell you want to observe next has the robot in it, 
			if (r != mazeDimension and mazeWalls[r][c][2] == 1 and mazeDepth[r][c-1] == scanDepth-1):  #LOOK SOUTH (from observed cell)
				if(scanDepth-1 == 0): 
					qtmp.put( [r,c])
					#pdb.set_trace()
					qtmp.queue=pathOptimizerObj.process(qtmp.queue) 
					return qtmp 
					#Return the next cell the robot should travel to. (if that cell is depth 0 (robot))
				qtmp.put( [r,c])
				c-= 1
			elif (r != -1 and mazeWalls[r][c][0] == 1 and mazeDepth[r][c+1] == scanDepth-1): #LOOK NORTH 
				if(scanDepth-1 == 0):
					qtmp.put( [r,c])
					#pdb.set_trace()
					qtmp.queue=pathOptimizerObj.process(qtmp.queue) 
					return qtmp 
				qtmp.put( [r,c])
				c += 1
			elif (c != mazeDimension and mazeWalls[r][c][1] == 1 and mazeDepth[r+1][c] == scanDepth-1): #LOOK EAST
				if(scanDepth-1 == 0): 
					qtmp.put( [r,c])
					#pdb.set_trace()
					qtmp.queue=pathOptimizerObj.process(qtmp.queue) 
					return qtmp 
				qtmp.put( [r,c])
				r += 1
			elif (c != -1 and mazeWalls[r][c][3] == 1 and mazeDepth[r-1][c] == scanDepth-1): #LOOK WEST
				if(scanDepth-1 == 0): 
					qtmp.put( [r,c])
					#pdb.set_trace()
					qtmp.queue=pathOptimizerObj.process(qtmp.queue) 
					return qtmp 
				qtmp.put( [r,c])
				r -= 1
			else:
				#print(qtmp.queue) 
				#print(mazeWalls[r][c]) 
				#print(r,c)
				#print(mazeDepth[r][c]) 
				#pdb.set_trace()
				#continue
				return qtmp
				 
			scanDepth -=1 #Seet the new depth of the observed cell.
	
		print(qtmp.queue)
		#pdb.set_trace()
		qtmp.queue=pathOptimizerObj.process(qtmp.queue) 
		return qtmp
	 
	 
		 
	 
	#set wall at given direction in a cell
	def cellSetWall(self, x, y, heading):
		#print(( x,y, heading))
		if(heading == "N"):
			self.wallSetN(x,y)
		elif(heading == "E"):
			self.wallSetE(x,y)
		elif(heading == "S"):
			self.wallSetS(x,y)
		elif(heading == "W"):
			 self.wallSetW(x,y)    

	def wallSetS(self,x,y):
		global mazeWalls
		mazeWalls[x][y][2] = 1
		if y > 0: # if there is then set the "same" wall in the cell right below (south wall)
			mazeWalls[x][y-1][0] = 1
		 
	def wallSetE(self,x,y):
		global mazeWalls
		mazeWalls[x][y][1] = 1
		if (x < len(mazeWalls[x])-1):
			mazeWalls[x+1][y][3] = 1
			 
	def wallSetN(self,x,y):
		global mazeWalls
		mazeWalls[x][y][0] = 1
		if (y < len(mazeWalls)-1): # if there is then set the "same" wall in the cell right above (south wall)
			mazeWalls[x][y+1][2] = 1
	 
	def wallSetW(self,x,y):
		global mazeWalls
		mazeWalls[x][y][3] = 1
		if (x > 0):
			mazeWalls[x-1][y][1] = 1
