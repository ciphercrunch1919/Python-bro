from SlidingTilePuzzle import *
from SlidingTileSolver import *
from PriorityQueue import *

from math import *

class MySolver(SlidingTileSolver):
   def __init__(self,problem,maxTime):
      SlidingTileSolver.__init__(self,problem,maxTime)
    # You need to redefine this function for your algorithm
    # It is currently using breadth-first search which is very slow
   def solve(self):
      frontier=PriorityQueue()
      frontier.push(0,(0,self._problem.getInitial()))
      seen=set()
      parent=dict()
      size = self._problem._size
      # Do not remove the timeRemaining check from the while loop
      while len(frontier)>0 and self.timeRemaining():
         self._numExpansions+=1
         priority,(depth,currentState)=frontier.pop()
         seen.add(currentState)
         for action in self._problem.actions(currentState):
            resultingState=self._problem.result(currentState,action)
            if self._problem.isGoal(resultingState):
               # Goal reached
               parent[resultingState]=(currentState,action)
               path=""
               current=resultingState
               while current!=self._problem.getInitial():
                  (current,action)=parent[current]
                  path=action+path
               return path
            if resultingState not in seen:
               #f=depth
               #h=self.heuristic(resultingState)
               frontier.push(depth+self.heuristic(resultingState,size),(depth+1,resultingState))
               seen.add(resultingState)
               parent[resultingState]=(currentState,action)
      return []
   def heuristic(self,state,size):
      lc=0
      mandist=0
      for i,e in enumerate(state):
         if e==0:
            continue
         if e==i:
            continue
         mandist+=abs(e//size-i//size)+abs(e%size-i%size)
         if(e-1)//size==(i+1)//size:
            lc+=2
         if(e-2)//size==(i+1)//size:
            lc+=1
         if(e+1)%size==(i-1)%size:
            lc+=2
         if(e+2)%size==(i-2)%size:
            lc+=1
      return max(mandist,((lc/(2*size))+mandist))
