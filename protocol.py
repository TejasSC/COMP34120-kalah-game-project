def createMoveMsg(hole):
    return "MOVE; " + hole + "\n"

def createSwapMsg():
    return "SWAP\n"

def getMessageType(msg):
    if "START;" in msg:
        return 0
    elif "CHANGE;" in msg:
        return 1
    elif "END\n" in msg:
        return 2
    else:
        raise ValueError("Could not determine message type.")

def interpretStartMsg(msg):
    if msg[len(msg)-1] != '\n':
        raise ValueError("Message not terminated")

    position = msg[6:len(msg)]
    if position == "South":
        return True
    elif position == "North":
        return False
    else:
        raise ValueError("Illegal position parameter: " + position)

#here holes will len(board.holes[0])
def interpretStateMsg(msg, holes):
    # [end, again, move]
    moveTurn = [False, False, 0]
    if msg[len(msg)-1] != '\n':
        raise ValueError("Message not terminated")

    parts = msg.split(";")

    if len(parts) != 4:
        raise ValueError("Missing arguments")

    if parts[1] == "SWAP":
        moveTurn[2] = -1;
    else:
        try:
            moveTurn[2] = int(parts[1])
        except ValueError:
            print("Move parameter set to illegal value")

    # 2nd argument = the board itself
    l = len(holes)
    boardParts = parts[2].split(",")
    n = 2*(l+1)
    if n != len(boardParts):
        raise ValueError("Board dimensions in message ("
            + str(boardParts.length) + " entries) are not as expected ("
            + str(n) + " entries).")

    try:
        #holes on the north side
        for i in range(0,l):
            board.setSeeds(1, i+1,int(boardParts[i]))
        board.setSeedsInWell(1, int(boardParts[l]))
        #holes on the south side
        for i in range(0,l):
            board.setSeeds(1, i+1,int(boardParts[i+l+1]))
        board.setSeedsInWell(1, int(boardParts[2*l+1]))
    except ValueError:
        print("Illegal value for seed count")


    # 3rd argument: who's turn is it
    if msgParts[3] == "YOU\n":
        moveTurn[1] = True
    else if msgParts[3] == "OPP\n":
        moveTurn[1] = False
    else if msgParts[3] == "END\n":
        moveTurn[0] = True
        moveTurn[1] = False
    else:
        raise ValueError("Illegal value for turn parameter")

    return moveTurn
