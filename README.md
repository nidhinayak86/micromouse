# MicroMouseAi 


install python 3 turtle library and other dependency libraries using pip3 
current code can only be run by python3 
 
To run program:-
python3 tester.py test_maze_01.txt  
python3 tester.py test_maze_02.txt  
python3 tester.py test_maze_03.txt  



To change code to still explore unexplored neighbourd after robot reached goal in trail mode 
robot.py:- 
self.exploreAfterGoalReached= False // change it to True



to change algorithm change do changes in 
robot.py:- 


line 19  :-          self.exploreAfterGoalReached= False # for maze exploration full/partial 


line 23 to 25 :-    to change maze algorithm 

 #self.algoObj=  AlgoPackage('floodfill' ,self.location, self.heading,self.goal_bounds, self.maze_dim ,self.exploreAfterGoalReached) 

 #self.algoObj=  AlgoPackage('dfs' ,self.location, self.heading,self.goal_bounds, self.maze_dim ,self.exploreAfterGoalReached ) 

 #self.algoObj=  AlgoPackage('bfs' ,self.location, self.heading,self.goal_bounds, self.maze_dim ,self.exploreAfterGoalReached) 



After code ends check:-
test score, train score and total score