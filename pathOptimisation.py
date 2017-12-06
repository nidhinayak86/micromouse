
from operator import itemgetter
import numpy as np


class pathOptimizer(object):
	def __init__(self):
		pass


	def traverse(self, lst):
		#lst=[(1,1),(1,2),(1,3),(1,4),(1,5),(2,5),(2,4),(2,3),(2,2),(3,2),(3,3),(3,4)]

		resultLst=[]
		for curr in lst:
			print(curr)

		print("----------------------------")
		a =  None
		b =  None
		c =  None
		thetaAB= None
		thetaBC= None
		initialize= 3
		current_count =1
		for curr in lst:

			if current_count <= 1:
				#print(curr)
				#print("S")
				#resultLst=resultLst+["S"]
				c=curr
				current_count =current_count+1
			elif(current_count <=2):
				#print(curr)
				b=curr
				current_count =current_count+1
				#print("calculating slope")
				thetaBC= self.slope(b[0], b[1], c[0], c[1])
				#print("S")
				resultLst=resultLst+["S"]
			elif(current_count<=3):
				#print(curr)
				a=curr
				current_count =current_count+1
				thetaAB= self.slope(b[0], b[1], a[0], a[1])
				if(thetaAB== thetaBC) :
					#print("S")
					resultLst=resultLst+["S"]
				else:
					#print("T")
					resultLst=resultLst+["T"]
			elif(curr==lst[len(lst)-1]):
				c=b
				b=a
				a=curr
				# check slopes
				thetaBC= self.slope(b[0], b[1], c[0], c[1])
				thetaAB= self.slope(b[0], b[1], a[0], a[1])
				if(thetaAB== thetaBC) :
					#print("S")
					resultLst=resultLst+["S"]
				else:
					#print("T")
					resultLst=resultLst+["T"]
				break
			else:
				c=b
				b=a
				a=curr
				# check slopes
				thetaBC= self.slope(b[0], b[1], c[0], c[1])
				thetaAB= self.slope(b[0], b[1], a[0], a[1])
				if(thetaAB== thetaBC) :
					#print("S")
					resultLst=resultLst+["S"]
				else:
					#print("T")
					resultLst=resultLst+["T"]
				pass
			
		print(resultLst)
		return resultLst


	def encodeLst(self, lst):
		current_count =0
		curr=None
		prev= None
		resultLst=[]
		for i in range(0, len(lst)):
			curr= lst[i]
			if( curr == "S" and i != len(lst)-1):
				current_count=current_count+1
			elif (curr != prev and prev != None and curr != "S"):
				resultLst=resultLst+[str(current_count)]+["S"] +["T"]
				current_count=0
			elif(curr == "S" and i == len(lst)-1):
				current_count=current_count+1
				resultLst=resultLst+[current_count]+[curr]
			else:
				resultLst=resultLst+[curr]

			prev= curr
		print(resultLst)
		return resultLst


	def minimumEncoding(self, coins,m, V):
		#pass
		#table[i] will be storing the minimum number of coins
		# required for i value.  So table[V] will have result
		table=[]
		# Base case (If given value V is 0)
		table = [0]	
		returnCoins = [[]] 
		# Initialize all table values as Infinite
		#for i=1; i<=V; i++)
		for i in range(1, V+1):
			table = table+[1000]
			tmpCoins=[]
			for j in range(0, m):
				tmpCoins=tmpCoins+[0]
			returnCoins=returnCoins+[tmpCoins]
			#print(returnCoins)

		#print(returnCoins)
		# Compute minimum coins required for all
		# values from 1 to V
		#for (int i=1; i<=V; i++)
		for i in range(1, V+1):
			# Go through all coins smaller than i
			#for (int j=0; j<m; j++)
			for j in range(0, m):
				if (coins[j] <= i):
					sub_res = table[i-coins[j]]
					if (sub_res != 1000 and sub_res + 1 < table[i]):
						table[i] = sub_res + 1
						#print(returnCoins[i-coins[j]])
						item= 0
						for item in returnCoins[i-coins[j]]:
							#print(item)
							if item != 0:
								break
						if item != 0:
							returnCoins[i][j]=[coins[j] ] + item
						else:
							returnCoins[i][j]=[coins[j] ]
						#returnCoins[i][j]=[coins[j] ] +returnCoins[i-coins[j]]

		#print("--final result------")
		#print(table[V])

		# for debugging
		"""
		for i in range( V, 1, -1):
			print(i)
			print(returnCoins[i])
		"""
		currentCount=1000
		result=None
		for item in returnCoins[V]:
			if item != 0 and len(item) < currentCount:
				currentCount= len(item)
				result= item

		#print(result)
		return result

	def convertEncoding(self, resultantLst ,lst):
		print(lst)
		result=[]
		for i in range(0, len(resultantLst)-1):
			if(resultantLst[i+1]=="S"):
				coins =  [3, 2, 1]
				m = 3
				V = int(resultantLst[i])
				optlst=self.minimumEncoding(coins, m, V)
				for j in optlst:
					result=result+[j]+["S"]
			elif(resultantLst[i]=="T"):
				result=result+["T"]
			else:
				pass
		print(result)
		#a=np.array(lst)
		#print(lst)
		#print(lst[3])
		outputPath=[]
		outputPath=outputPath +[lst[0]]
		runningCount=1
		for i in range(0, len(result)):
			
			if(i!=len(result)-1 and result[i+1]=="S"):
				#print("---------")
				#print(i)
				#print(runningCount)
				#print(lst[int(result[i])+ runningCount-1])
				outputPath=outputPath +[lst[int(result[i])+runningCount-1]]
				runningCount=runningCount+int(result[i]) 
			elif(result[i]=="T"):
				#print("***********")
				#print(i)
				#print(runningCount)
				#print(lst[runningCount])
				outputPath=outputPath+[lst[runningCount]]
				runningCount=runningCount+1
			else:
				pass

		outputPath=outputPath+[lst[len(lst)-1]]
		print(outputPath)
		return outputPath

	#in maze robot going only left right, up down so slope
	#only in 0 or 90
	def slope(self, x1, y1, x2, y2):
		if x1 != x2:
			return 0
		else:
			return 90

	def process(self, lst):
		print("#######################  path optimiser ######################")
		lst=list(reversed(lst))
		print(lst)
		resultantLst=self.traverse(lst)
		resultantLst=self.encodeLst(resultantLst)
		
		lst=list(reversed(self.convertEncoding(resultantLst ,lst)))
		return lst

	def test(self ):
		lst=[(1,1),(1,2),(1,3),(1,4),(1,5),(2,5),(2,4),(2,3),(2,2),(3,2),(3,3),(3,4)]
		self.process(lst)

if __name__ == '__main__':
	lst=[[6, 5], [6, 6], [7, 6], [7, 5], [8, 5], [8, 4], [8, 3], [9, 3], [10, 3], [11, 3], [11, 2], [11, 1], [11, 0], [10, 0], [9, 0], [8, 0], [7, 0], [7, 1], [6, 1], [6, 2], [5, 2], [4, 2], [4, 1], [4, 0], [3, 0], [2, 0], [1, 0], [1, 1], [1, 2], [0, 2], [0, 1]]	
	obj = pathOptimizer()
	obj.process(lst)

#"""
	


"""
[6, 5]
[6, 6]
[7, 6]
[7, 5]
[8, 5]
[8, 4]
[8, 3]
[9, 3]
[10, 3]
[11, 3]
[11, 2]
[11, 1]
[11, 0]
[10, 0]
[9, 0]
[8, 0]
[7, 0]
[7, 1]
[6, 1]
[6, 2]
[5, 2]
[4, 2]
[4, 1]
[4, 0]
[3, 0]
[2, 0]
[1, 0]
[1, 1]
[1, 2]
[0, 2]
[0, 1]
----------------------------
['S', 'T', 'T', 'T', 'T', 'S', 'T', 'S', 'S', 'T', 'S', 'S', 'T', 'S', 'S', 'S', 'T', 'T', 'T', 'T', 'S', 'T', 'S', 'T', 'S', 'S', 'T', 'S', 'T', 'T']
['1', 'S', 'T', 'T', 'T', 'T', '1', 'S', 'T', '2', 'S', 'T', '2', 'S', 'T', '3', 'S', 'T', 'T', 'T', 'T', '1', 'S', 'T', '1', 'S', 'T', '2', 'S', 'T', '1', 'S', 'T', 'T']
[[6, 5], [6, 6], [7, 6], [7, 5], [8, 5], [8, 4], [8, 3], [9, 3], [10, 3], [11, 3], [11, 2], [11, 1], [11, 0], [10, 0], [9, 0], [8, 0], [7, 0], [7, 1], [6, 1], [6, 2], [5, 2], [4, 2], [4, 1], [4, 0], [3, 0], [2, 0], [1, 0], [1, 1], [1, 2], [0, 2], [0, 1]]
[[6, 5], [6, 6], [7, 6], [7, 5], [8, 5], [8, 4], [8, 3], [9, 3], [10, 3], [11, 3], [11, 2], [11, 1], [11, 0], [10, 0], [9, 0], [8, 0], [7, 0], [7, 1], [6, 1], [6, 2], [5, 2], [4, 2], [4, 1], [4, 0], [3, 0], [2, 0], [1, 0], [1, 1], [1, 2], [0, 2], [0, 1]]
[1, 'S', 'T', 'T', 'T', 'T', 1, 'S', 'T', 2, 'S', 'T', 2, 'S', 'T', 3, 'S', 'T', 'T', 'T', 'T', 1, 'S', 'T', 1, 'S', 'T', 2, 'S', 'T', 1, 'S', 'T']
[[6, 5], [6, 6], [7, 6], [7, 5], [8, 5], [8, 4], [8, 3], [9, 3], [11, 3], [11, 2], [11, 0], [10, 0], [7, 0], [7, 1], [6, 1], [6, 2], [5, 2], [4, 2], [4, 1], [4, 0], [3, 0], [1, 0], [1, 1], [1, 2], [0, 2], [0, 1]]
('Reset', 'Reset')

"""