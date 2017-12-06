import numpy as np
from maze import Maze
import random
import turtle
import sys
from floodfill import floodFill
import djkistra
from depthFirstSearch import dfs
from bfs import bfs

class AlgoPackage(object):
	def __init__(self, typeOfAlgo , location, heading,goal_bounds, mazeDim, exploreAfterGoalReached):

		"""
		taking type of algo
		"""
		print((typeOfAlgo , location, heading,goal_bounds, mazeDim))
		self.algoType = typeOfAlgo
		self.mazeDim = mazeDim
		self.algoObj = None
		self.location =  location
		self.heading = heading
		self.goal_bounds = goal_bounds
		self.exploreAfterGoalReached=exploreAfterGoalReached
		#self.graphAdjacencyMatrix=self.buildAdjacencyGraph(self.mazeObj)
		if self.algoType == "Djskitra":
			self.algoObj = Djkistra(location, heading, goal_bounds, self.mazeDim ,exploreAfterGoalReached  )
		elif self.algoType == "floodfill":
			self.algoObj =  floodFill(location, heading, goal_bounds, self.mazeDim ,exploreAfterGoalReached)	
		elif self.algoType == "dfs":
			self.algoObj =  dfs(location, heading, goal_bounds, self.mazeDim ,exploreAfterGoalReached)	
		elif self.algoType == "bfs":
			self.algoObj =  bfs(location, heading, goal_bounds, self.mazeDim ,exploreAfterGoalReached)	
		elif self.algoType == "random":
			self.algoObj= None
		else:
			print("No specific  algorithm  mentioned")

		


	def callRandom(self ,sensing):
		print("calling random algo")
		possible_movement = [-3, -2, -1, 0, 1 , 2,3]
		possible_rotation=[-90 ,0 ,90]
		return (random.choice(possible_rotation) ,random.choice(possible_movement))



	def callFloodfill(self , sensing ,location,direction ,oldLocation ,oldHeading):
		print("calling floodfill algo")
		(rotation,movement)=self.algoObj.nextStep(sensing ,location,direction ,oldLocation ,oldHeading)

		print((rotation,movement))
		return (rotation,movement)


	def callDfs(self , sensing ,location,direction ,oldLocation ,oldHeading):
		print("calling DFS algo")
		(rotation,movement)=self.algoObj.nextStep(sensing ,location,direction ,oldLocation ,oldHeading)

		print((rotation,movement))
		return (rotation,movement)

	def callBfs(self , sensing ,location,direction ,oldLocation ,oldHeading):
		print("calling BFS algo")
		(rotation,movement)=self.algoObj.nextStep(sensing ,location,direction ,oldLocation ,oldHeading)
		print((rotation,movement))
		return (rotation,movement)

	def callDjkistra(self ,sensing):
		print( "calling djisktra shortest path for non negative weights")
		pass


	def nextMove(self , sensing ,location,direction ,oldLocation ,oldHeading):
		print(sensing)
		if self.algoType == "djskitra":
			return self.callDjkistra(sensing)

		elif self.algoType == "random":
			return self.callRandom(sensing)

		elif self.algoType == "floodfill":
			return self.callFloodfill(sensing ,location,direction ,oldLocation ,oldHeading)
			
		elif self.algoType == "dfs":
			return self.callDfs(sensing ,location,direction ,oldLocation ,oldHeading)	

		elif self.algoType == "bfs":
			return self.callBfs(sensing ,location,direction ,oldLocation ,oldHeading)
		else:
			print("No specific  algorithm  mentioned")




