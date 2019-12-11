import protocol as pr
import kalah as k

def communicate():
    try:
        while True:
            print("\n")
            # how the fuck do we do this bit ooooooooooof
            msg = input("Enter your message here: ")
            # a confirmation that we've received the message
            print("Received: \n" + msg)
            try:
                mt = pr.getMessageType(msg)
                if mt == 0:
                    #start msg
                    first = pr.interpretStartMsg(msg)
                    if first:
                        print("\nStarting player is south")
                    else:
                        print("\nStarting player is north")
                elif mt == 1:
                    print("\nA start.")
                    b = k.Board()
                    numHoles = len(b.holes[0])
                    moveTurn = pr.interpretStateMsg(msg,numHoles)
                    print("\nThis move was: " + moveTurn[2])
                    print("\nIs the game over? " + moveTurn[0])
                    if not moveTurn[0]:
                        print("\nIs it our turn again? " + moveTurn[1])
                    print("\nThe board:\n" + str(b))
                else:
                    print("\nAn end. Bye bye!")
            except Exception as e:
                raise
    except Exception as e:
        raise
