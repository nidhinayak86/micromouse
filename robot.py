import numpy as np
import random
from algo import AlgoPackage

class Robot(object):
    def __init__(self, maze_dim):
        '''
        Use the initialization function to set up attributes that your robot
        will use to learn and navigate the maze. Some initial attributes are
        provided based on common information, including the size of the maze
        the robot is placed in.
        '''

        self.location = [0, 0]
        self.heading = 'up'
        self.maze_dim = maze_dim
        self.oldLocation=[0, 0]
        self.oldheading='up'
        self.exploreAfterGoalReached= True
            # check for goal entered
        self.goal_bounds = [int(maze_dim/2) - 1, int(maze_dim/2)]
        #self.algoObj=  AlgoPackage('random' ,self.location, self.heading,self.goal_bounds, self.maze_dim ,self.exploreAfterGoalReached)
        self.algoObj=  AlgoPackage('floodfill' ,self.location, self.heading,self.goal_bounds, self.maze_dim ,self.exploreAfterGoalReached)
        #self.algoObj=  AlgoPackage('dfs' ,self.location, self.heading,self.goal_bounds, self.maze_dim ,self.exploreAfterGoalReached )
        #self.algoObj=  AlgoPackage('bfs' ,self.location, self.heading,self.goal_bounds, self.maze_dim ,self.exploreAfterGoalReached)



    def next_move(self, sensors):
        '''
        Use this function to determine the next move the robot should make,
        based on the input from the sensors after its previous move. Sensor
        inputs are a list of three distances from the robot's left, front, and
        right-facing sensors, in that order.

        Outputs should be a tuple of two values. The first value indicates
        robot rotation (if any), as a number: 0 for no rotation, +90 for a
        90-degree rotation clockwise, and -90 for a 90-degree rotation
        counterclockwise. Other values will result in no rotation. The second
        value indicates robot movement, and the robot will attempt to move the
        number of indicated squares: a positive number indicates forwards
        movement, while a negative number indicates backwards movement. The
        robot may move a maximum of three units per turn. Any excess movement
        is ignored.

        If the robot wants to end a run (e.g. during the first training run in
        the maze) then returing the tuple ('Reset', 'Reset') will indicate to
        the tester to end the run and return the robot to the start.
        '''
        (rotation,movement) = self.algoObj.nextMove(sensors ,self.location,self.heading ,self.oldLocation,self.oldheading )
        print(("robot rotation =" ,rotation))
        print(("robot movement=" ,movement))

        #rotation = 0
        #movement = 0

        if rotation=='Reset' and movement== 'Reset':
            self.update_move( [0,0] , 'up')

        return rotation, movement


    def update_move(self, currlocation , currdirection):
        self.oldLocation=self.location
        self.oldheading=self.heading
        self.location = currlocation
        self.heading = currdirection