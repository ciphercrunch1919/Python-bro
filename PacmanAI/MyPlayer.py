from Player import * 

import random

class MyPlayer(Player):
  def __init__(self, timeLimit):
    Player.__init__(self, timeLimit)
  
  #from slides 
  def findMove(self, state):
    #iterative deepening
    depth = 0
    while self.timeRemaining():
      v, m = self.maxPlayerValue(state, depth)
      if not m:
         return
      self.setMove(m)
      depth += 1

  def maxPlayerValue(self, state, depth):
    if state.gameOver():
      return state.getScore(), None
    if depth == 0:
      return self.heuristic(state)

    best = -100000
    bestMove = None
    for m, action in enumerate(state.actions()):
      if action == 'Stay':
        continue
      result = state.result(action)
      v = self.randomPlayerValue(result, depth-1)
      if (v > best):
        best = v
        bestMove = action

    return best, bestMove

  def randomPlayerValue(self, state, depth):
    if state.gameOver():
      return state.getScore()
    if depth == 0:
      return self.heuristic(state)[0]

    average = 0
    for i, (result, prob) in enumerate(state.ghostResultDistribution()):
      v = self.maxPlayerValue(result, depth-1)[0]
      average += prob * v

    return average

  #my heuristic
  def heuristic(self, state):
    score = -100000
    pacAction = None
    for m, action in enumerate(state.actions()):
       if action == 'Stay':
         continue

       pacman = state.getPlayerPosition()
       powerups = state.getPowerUps()
       newScore = state.result(action).getScore()

       if (len(powerups) == 0):
         newScore = self.findFood(state, pacman, newScore)

       if len(powerups) > 0:
         newScore = self.findPowerUps(state, powerups, pacman, newScore)

       if state.getScaredTurnsLeft() > 4:
         newScore += self.findGhosts(state, pacman, newScore)

       if newScore > score:
         score = newScore
         pacAction = action

    return score, pacAction

  #finding the food
  def findFood(self, state, pacman, currentScore):
    foods = state.getPellets()

    closest = 100
    for i, food in enumerate(foods):
      if state._map.mapDistance(pacman, food) < closest:
        closest = state._map.mapDistance(pacman, food)
    currentScore += 9/closest

    if closest != 1:
      currentScore -= 1

    return currentScore

  #finding the ghosts during scared time
  def findGhosts(self, state, pacman, currentScore):
    ghosts = state.getGhostPositions()

    closest = 100
    for j, ghost in enumerate(ghosts):
      if state._map.mapDistance(pacman, ghost) < closest:
        closest = state._map.mapDistance(pacman, ghost)
    if closest == 0:
      closest = 1
    currentScore += 200/closest      

    return currentScore

  #finding the powerups
  def findPowerUps(self, state, powerups, pacman, currentScore):
    ghosts = state.getGhostPositions()

    closest = 100
    if state._map.mapDistance(pacman, ghosts[0]) < 5:
      for k, powerup in enumerate(powerups):
        if state._map.mapDistance(pacman, powerup) < closest:
          closest = state._map.mapDistance(pacman, powerup)
      currentScore += 200/closest
    
    return currentScore
