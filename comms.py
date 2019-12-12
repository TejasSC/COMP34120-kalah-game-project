#!/usr/bin/env python3
import sys
import protocol as pr
import kalah as k

def communicate():
    try:
        while True:
            print("\n")
            for msg in sys.stdin:
                msg = input("Enter your message here: ")
                print(msg)
                # a confirmation that we've received the message
                print("Received: " + msg + "\n")
                try:
                    mt = pr.getMessageType(msg)
                    if mt == 0:
                        #start msg
                        first = pr.interpretStartMsg(msg)
                        if first:
                            print("Starting player is south\n")
                        else:
                            print("Starting player is north\n")
                    elif mt == 1:
                        print("A start.\n")
                        b = k.Board()
                        numHoles = len(b.holes[0])
                        moveTurn = pr.interpretStateMsg(msg,numHoles)
                        print("This move was: " + moveTurn[2] + "\n")
                        print("Is the game over? " + moveTurn[0] + "\n")
                        if not moveTurn[0]:
                            print("Is it our turn again? " + moveTurn[1] + "\n")
                            print("The board:\n" + str(b) + "\n")
                        else:
                            print("An end. Bye bye!\n")
                except Exception as e:
                    raise
    except Exception as e:
        raise
