from copy import deepcopy

# sides of board
SOUTH = 1
NORTH = 0

# states of game
START = 0
STATE = 1
END = 2

HOLES = 7
SEEDS = 7

class Move(object):
    """docstring for Move."""

    def __init__(self, side, hole):
        self.side = side
        self.hole = hole
    def __str__(self):
        return "Side {0}, hole {1}".format(self.side, self.hole)

class Board(object):
    """docstring for Board."""

    def __init__(self, holes = None):
        if holes is None:
            self.makeNewBoard(7,7)
        else:
            self.holes = holes

    def makeMove(self, move):
        side, hole = move.side, move.hole
        if hole < 1:
            raise ValueError("Invalid move")

    def makeNewBoard(self,numHoles,seeds):
        if numHoles < 1:
            raise ValueError("Must be at least one hole")
        if seeds < 0:
            raise ValueError("Must be non negative number of seeds per hole")
        #make board
        self.holes = [[0] + [seeds]*numHoles, [0] + [seeds]*numHoles]

    def __str__(self):
        return (
          "    {6:2d} {5:2d} {4:2d} {3:2d} {2:2d} {1:2d} {0:2d}\n".format(*self.holes[1])
        + "{0:2d}                   {1:2d}\n".format(self.wells[1], self.wells[0])
        + "   {0:2d} {1:2d} {2:2d} {3:2d} {4:2d} {5:2d} {6:2d}".format(*self.holes[0])
        )#

    def getSeeds(self, side, hole):
        if hole < 1 or hole > len(self.holes[0]):
            raise ValueError("hole must be between 1 and " + str(l))
        if seeds < 0:
            raise ValueError("Must be non negative number of seeds per hole")
        return self.holes[side][hole]

    def setSeeds(self, side, hole, seeds):
        if hole < 1 or hole > len(self.holes[0]):
            raise ValueError("hole must be between 1 and " + str(l))
        if seeds < 0:
            raise ValueError("Must be non negative number of seeds per hole")
        self.holes[side][hole] = seeds

    def addSeeds(self, side, hole, seeds):
        if hole < 1 or hole > len(self.holes[0]):
            raise ValueError("hole must be between 1 and " + str(l))
        if seeds < 0:
            raise ValueError("Must be non negative number of seeds per hole")
        self.holes[side][hole] += seeds

    def getSeedsOpp(self, side, hole):
        if hole < 1 or hole > len(self.holes[0]):
            raise ValueError("hole must be between 1 and " + str(l))
        return self.holes[1-side][HOLES+1-hole]

    def setSeedsOpp(self, side, hole, seeds):
        setSeeds(1-side,HOLES+1-hole,seeds)

    def addSeedsOpp(self, side, hole, seeds):
        addSeeds(1-side,HOLES+1-hole,seeds)

    def getSeedsInWell(self, side):
        return self.holes[side][0]

    def setSeedsInWell(self, side, seeds):
        if seeds < 0:
            raise ValueError("Must be non negative number of seeds per hole")
        self.holes[side][0] = seeds

    def addSeedsToWell(self, side, seeds):
        if seeds < 0:
            raise ValueError("Must be non negative number of seeds per hole")
        self.holes[side][0] += seeds

class Kalah(object):
    """docstring for Kalah."""
    def __init__(self, board):
        self.board = board
    def moveAllowed(self, board, move):
        return (move.hole <= len(board.holes[0])) and (board.getSeeds(move.side, move.hole) != 0)

    # returns a side, i.e. north or south
    def makeMove(self, board, move):
        seedsToSow = board.getSeeds(move.side, move.hole)
        board.setSeeds(move.side, move.hole, 0)
        numHoles = len(board.holes[0])
        pits = 2*numHoles + 1 #sow into all holes + 1 well
        rounds = int(numHoles/pits)
        extra = numHoles % pits

        if rounds != 0:
            for hole in range(1, numHoles+1):
                board.addSeeds(NORTH, hole, rounds)
                board.addSeeds(SOUTH, hole, rounds)
            board.addSeedsToWell(move.side, rounds)

        #sow extra seeds
        sowSide = move.side
        sowHole = move.hole # the well is represented with 0
        for i in range(extra, 0, -1):
            sowHole+=1
            if sowHole == 1:
                sowSide = 1 - sowSide #if the last pit was a well
            if sowHole > numHoles:
                if sowSide == move.side:
                    sowHole = 0#sow to the well now
                    board.addSeedsToWell(sowSide, 1)
                else:
                    sowSide = 1 - sowSide
                    sowHole = 1
            board.addSeeds(sowSide, sowHole, 1)

        #capture
        #last seed was sown on the moving player's side
        if (sowSide == move.side) and (sowHole > 0) and(board.getSeeds(sowSide, sowHole)) and (board.getSeedsOpp(sowSide, sowHole)):
            board.addSeedsToWell(move.side, 1+board.getSeedsOpp(move.side, sowHole))
            board.setSeeds(move.side, sowHole, 0)
            board.setSeedsOpp(move.side, sowHole, 0)

        finishedSide = 0
        if holesEmpty(board, move.side):
            finishedSide = move.side
        elif holesEmpty(board, 1 - move.side):
            finishedSide = 1 - move.side

        seeds = 0
        collectingSide = 1 - finishedSide
        if finishedSide != 0:
            for hole in range(1, numHoles+1):
                seeds+= board.getSeeds(collectingSide, hole)
                board.setSeeds(collectingSide, hole, 0)
            board.addSeedsToWell(collectingSide, seeds)

        # notify observers i guess idk
        # decide turn
        if sowHole == 0:
            return move.side
        else:
            return 1 - move.side

    def holesEmpty(board, side):
        for hole in range(1, hole+1):
            if(board.getSeeds(sides, hole) != 0):
                return False
        return True

    def gameOver(arg):
        return holesEmpty(board, 0) or holesEmpty(board, 1)
