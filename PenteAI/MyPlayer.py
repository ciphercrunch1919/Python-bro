import random
from Pente import *

class MyPlayer(Player):
   def __init__(self, timeLimit):
      Player.__init__(self, timeLimit)

   def findMove(self, state):
      depth = 1
      while self.timeRemaining():
         print('Depth', depth)
         if state.getTurn() % 2 == 0:
            (v, m) = self.maxPlayer(state, depth, -1e6, 1e6)
            self.setMove(m)
         else:
            (v, m) = self.minPlayer(state, depth, -1e6, 1e6)
            self.setMove(m)

         depth += 1
         print(state.moveToStr(m), v)

   def maxPlayer(self, state, depth, alpha, beta):
      if state.gameOver():
         return (1 - state.winner(), tuple())

      if depth == 0: 
         return (self.heuristic(state),tuple())
    
      actions = state.actions()
      
      best = (-1e6, tuple())
      for a in actions:
         result = state.result(a)
         (v, m) = self.minPlayer(result, depth-1, alpha, beta)
      
         if v > beta: 
            return (v, a)
      
         best = max(best, (v,a))
         alpha = max(alpha, v)
        
      return best

   def minPlayer(self, state, depth, alpha, beta):
      if state.gameOver():
         return (1 - state.winner(), tuple())
      if depth == 0: 
         return (self.heuristic(state),tuple())
    
      actions = state.actions()
      
      best = (1e6, tuple())
      for a in actions:
         result = state.result(a)
         (v, m) = self.maxPlayer(result, depth-1, alpha, beta)
      
         if v < alpha: 
            return (v, a)
      
         best = min(best, (v,a))
         beta = min(beta, v)
      
      return best
    
   def heuristic(self, state):
      value = 0.5

      if state.getTurn() % 2 == 0:
         value += (0.05 *state.patternCount("BBBB ")) - (0.025 * state.patternCount("WWWW "))
         value += (0.2 * state.patternCount(" BBBB ")) - (0.1 * state.patternCount(" WWWW "))
         value += (0.1 * state.patternCount(" BBB ")) -( 0.05 * state.patternCount(" WWW "))
         value += (0.1 * state.patternCount(" BB B")) - (0.05 * state.patternCount(" WW W"))
         value += (0.05 * (state.getCaptures()[0]+1)) - (0.25 * (state.getCaptures()[1]+1))
         value += (0.006 * state.patternCount(" BB ")) - (0.003 * state.patternCount(" WW "))
         value += (0.006 * state.patternCount(" B B ")) - (0.003 * state.patternCount(" W W "))
         value += (0.013 * state.patternCount("BWW ") * (state.getCaptures()[0] + 1)) - (0.006 * state.patternCount("WBB ") * (state.getCaptures()[1] +1))
      else:
         value += (0.025 * state.patternCount("BBBB ")) - (0.05 * state.patternCount("WWWW "))
         value += (0.1 * state.patternCount(" BBBB ")) - (0.2 * state.patternCount(" WWWW "))
         value += (0.05 * state.patternCount(" BBB ")) - (0.1 * state.patternCount(" WWW "))
         value += (0.05 * state.patternCount(" BB B")) - (0.1 * state.patternCount(" WW W"))
         value += (0.25 * (state.getCaptures()[0]+1)) - (0.05 * (state.getCaptures()[1]+1))
         value += (0.003 * state.patternCount(" BB ")) -(0.006 * state.patternCount(" WW "))
         value += (0.003 * state.patternCount(" B B ")) - (0.006 * state.patternCount(" W W "))
         value += (0.006 * state.patternCount("BWW ") * (state.getCaptures()[0] + 1)) - (0.013 * state.patternCount("WBB ") * (state.getCaptures()[1] +1))

      if value > 1 or value == 0:
         return 0.5

      return value
