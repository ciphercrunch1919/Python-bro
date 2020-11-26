import random

from Pente import *

class colemanem(Player):
   def __init__(self, timeLimit):
      Player.__init__(self, timeLimit)
      self._mem = {}

   def findMove(self, state):
      depth = 1
      v = 0.5
      while((0.001 < v < 0.999) and (self.timeRemaining())):
         #print('Depth', depth)
         if state.getTurn() % 2 == 0:
            (v, m) = self.maxPlayer(state, depth, -1e6, 1e6)
            self.setMove(m)
         else:
            (v, m) = self.minPlayer(state, depth, -1e6, 1e6)
            self.setMove(m)

         depth += 1
         #print(state.moveToStr(m), v)

   def maxPlayer(self, state, depth, alpha, beta):
      if state.gameOver():
         if state.winner() == 0:
            return ((1 - 1e-6*state.getTurn()), tuple())
         else:
            return ((0 + 1e-6*state.getTurn()), tuple())
         return (0.5, None)

      if depth == 0: 
         return (self.heuristic(state),tuple())
    
      actions = self.moveOrder(state)
      if len(actions) == 0:
         actions = state.actions()

      best = (-1e6, tuple())
      for i,a in enumerate(actions):
         result = state.result(a)
         (v, m) = self.minPlayer(result, depth-1, alpha, beta)
      
         if v > beta: 
            return (v, a)
      
         best = max(best, (v,a))
         alpha = max(alpha, v)

      return best

   def minPlayer(self, state, depth, alpha, beta):
      if state.gameOver():
         if state.winner() == 0:
            return ((1 - 1e-6*state.getTurn()), tuple())
         else:
            return ((0 + 1e-6*state.getTurn()), tuple())
         return (0.5, None)

      if depth == 0: 
         return (self.heuristic(state),tuple())
    
      actions = self.moveOrder(state)
      if len(actions) == 0:
         actions = state.actions()
         
      best = (1e6, tuple())
      for i,a in enumerate(actions):
         result = state.result(a)
         (v, m) = self.maxPlayer(result, depth-1, alpha, beta)
      
         if v < alpha: 
            return (v, a)
      
         best = min(best, (v,a))
         beta = min(beta, v)
      
      return best

   def moveOrder(self, state):
      if state in self._mem:
         return self._mem[state]
      moveValue = dict()

      win = state.winningMoves()
      if len(win) > 0:
         return win

      block = state.blockingMoves()
      if len(block) > 0:
         return block

      for i,m in enumerate(state.patternLocations("BB_")):
         moveValue[m] = moveValue.get(m, 0) + 96
      for i,m in enumerate(state.patternLocations("WW_")):
         moveValue[m] = moveValue.get(m, 0) + 96
      for i,m in enumerate(state.patternLocations("B _B")):
         moveValue[m] = moveValue.get(m, 0) + 412
      for i,m in enumerate(state.patternLocations("W _W")):
         moveValue[m] = moveValue.get(m, 0) + 412
      for i,m in enumerate(state.patternLocations("B_B")):
         moveValue[m] = moveValue.get(m, 0) + 256
      for i,m in enumerate(state.patternLocations("W_W")):
         moveValue[m] = moveValue.get(m, 0) + 256
      for i,m in enumerate(state.patternLocations("BB_B")):
         moveValue[m] = moveValue.get(m, 0) + 796
      for i,m in enumerate(state.patternLocations("WW_W")):
         moveValue[m] = moveValue.get(m, 0) + 796
      for i,m in enumerate(state.patternLocations("BBB_")):
         moveValue[m] = moveValue.get(m, 0) + 1024
      for i,m in enumerate(state.patternLocations("WWW_")):
         moveValue[m] = moveValue.get(m, 0) + 1024
      for i,m in enumerate(state.patternLocations("BWW_")):
         moveValue[m] = moveValue.get(m, 0) + 512*(state.getCaptures()[0]+1)
      for i,m in enumerate(state.patternLocations("WBB_")):
         moveValue[m] = moveValue.get(m, 0) + 512*(state.getCaptures()[1]+1)
      for i,m in enumerate(state.patternLocations(" BBB_w")):
         moveValue[m] = moveValue.get(m, 0) + 4096
      for i,m in enumerate(state.patternLocations(" WWW_b")):
         moveValue[m] = moveValue.get(m, 0) + 4096
      for i,m in enumerate(state.patternLocations(" BB_w")):
         moveValue[m] = moveValue.get(m, 0) + 128
      for i,m in enumerate(state.patternLocations(" WW_b")):
         moveValue[m] = moveValue.get(m, 0) + 128
      for i,m in enumerate(state.patternLocations("B_")):
         moveValue[m] = moveValue.get(m, 0) + 16
      for i,m in enumerate(state.patternLocations("W_")):
         moveValue[m] = moveValue.get(m, 0) + 16
      for i,m in enumerate(state.patternLocations("B _")):
         moveValue[m] = moveValue.get(m, 0) + 4
      for i,m in enumerate(state.patternLocations("W _")):
         moveValue[m] = moveValue.get(m, 0) + 4

      candidates = []
      for i,(k,v)  in enumerate(moveValue.items()):
         candidates.append((-v + random.random()*1e-4, k))
         random.shuffle(candidates)
      candidates.sort()
      if len(candidates) > 10:
         candidates = candidates[:10]     

      self._mem[state] = [m for (v,m) in candidates]
      return [m for (v,m) in candidates]

   def heuristic(self, state):
      value = 0.5

      black = state.patternCount("bbbbb")/(state.patternCount("bbbbb") + state.patternCount("wwwww"))
      dem = state.getCaptures()[0] + state.getCaptures()[1]
      if dem == 0:
         dem = 0.5

      cap = state.getCaptures()[0]/dem
      value = (black+cap)/2

      return value
