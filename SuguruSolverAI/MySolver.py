from SuguruSolver import *

class MySolver(SuguruSolver):
    def __init__(self, problem, maxTime, visualizer):
        SuguruSolver.__init__(self, problem, maxTime, visualizer)
    
    # You should improve these functions to improve performance
    def selectUnassignedLocation(self, state):
        # Find the first location on the board has more than one possibility
        # then return it.  In class we talked about heuristics that might 
        # perform better than this.

        
        sm = 6
        loc = (0,0)
        t = True

        for row in range(self._problem.getSize()[0]):
            for col in range(self._problem.getSize()[1]):
                if (len(state.getPossibleValues((row,col))) < sm ) and (len(state.getPossibleValues((row,col))) > 1):
                    sm = len(state.getPossibleValues((row,col)))
                    loc = (row,col)

        return loc

    def isConsistent(self, state, location, value):
        # Check if putting value at location on the board is consistent
        # with the problem constraints.  This needs to be implemented.
        # Right now it says that it is always consistent.
        #checking cells for consistency
        cellid = state.getCellId(location)
        cell = state.getCell(cellid)
        row, col = state.getSize()
        x, y = location[1], location[0]

        for pos1 in range(-1,2):
            for pos2 in range(-1,2):
                if(y+pos1 > -1 and y+pos1 < row)and(x+pos2 > -1 and x+pos2 < col):
                    nloc = (y+pos1, x+pos2)
                    posvalue2 = state.getPossibleValues(nloc)[0]
                    if(nloc == (y,x)):
                        continue
                    if (y,x) in cell:
                        continue
                    if state.isValueKnown(nloc):
                        if posvalue2 == value:
                            #input("HIT ENTER")
                            return False 

        for i, loc in enumerate(cell):
            #print(loc)
            posvalue1 = state.getPossibleValues(loc)[0]
            if loc == (y,x):
                continue
            if state.isValueKnown(loc):
                if posvalue1 == value:
                    #input("HIT ENTER")
                    return False

       #input("HIT ENTER")
        return True

    def infer(self, state, changedLocations, initial=False):
        while len(changedLocations) > 0:
            row, col = state.getSize()
            cloc = changedLocations.pop()
            if(state.getPossibleValues(cloc) == []):
                continue
            x, y = cloc[1], cloc[0]
            posvalue = state.getPossibleValues(cloc)[0]
            cell = state.getCell(state.getCellId(cloc))
            cellsize = state.cellSize(state.getCellId(cloc))

            for i, loc in enumerate(cell):
                if loc == cloc:
                    continue
                if posvalue in state.getPossibleValues(loc):
                    state.removePossibleValue(loc, posvalue)
                    if state.isValueKnown(loc):
                        #print("here",loc)
                        changedLocations.append(loc)

            for pos1 in range(-1,2):
                for pos2 in range(-1,2):
                    if(y+pos1 > -1 and y+pos1 < row)and(x+pos2 > -1 and x+pos2 < col):
                        nloc = (y+pos1, x+pos2)
                        #print("NLOC: ", nloc, "CLOC: ",cloc, "value: ", posvalue)
                        if nloc == cloc:
                            continue
                        if nloc in cell:
                            continue
                        if posvalue in state.getPossibleValues(nloc):
                            state.removePossibleValue(nloc, posvalue)
                            if state.isValueKnown(nloc):
                                #print("here",nloc)
                                changedLocations.append(nloc)
        #input("HIT ENTER")
        return state
