maxTime = 300 #int(input('Enter the time limit: '))
puzzle = "1506AA0AB0AB0AB1AC0AC0AA0AU0AB0AC0AC5AD0AA0AU0AU0AE0AC0AD0AA0AU0AE0AE0AE0AG0AA4AU0AF0AE3AG0AG0AH0AF0AF0AF0AG0AK0AH0AI0AF4AJ0AG0AK0AH0AL0AJ0AJ0AJ5AK0AH0AL0AL0AJ0AN0AK4AH0AL0AM0AN0AN0AK0AQ0AL0AM0AN3AO0AO0AQ0AQ3AP0AN0AO0AO4AQ0AP0AP0AP0AS5AO0AQ0AR5AP0AS0AS0AS0AR0AR0AR0AR0AS0AT0-b4a34c99b5b39240661edc11802d087d" #input('Entry the string encoding for the puzzle: ')
graphics = 0 #int(input('Enter the size of the graphics window (0 for no graphics) '))

from MySolver import *
from Suguru import *

p = Suguru(suguruFromString(puzzle))
if graphics > 0:
   from SuguruVisualizer import *
   visualizer = SuguruVisualizer(p.getInitial(), graphics)
else:
   visualizer = None
print('Solving puzzle:')

solution=MySolver(p, maxTime, visualizer).solution()

import hashlib

solutionHash = hashlib.md5(str(solution).encode()).hexdigest()
if solutionHash == puzzle.split('-')[1]:
   print('Correct solution')
else:
   print('Solution is incorrect')

if visualizer and solution and solution.isGoal():
   visualizer.draw(solution)
