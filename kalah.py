#!/usr/bin/python
import random as rd
from copy import deepcopy
             
holes = 7
beans = 7
south = 1
north = 0

class Kalah(object):
    """docstring for Kalah."""

    def __init__(self, holesB = None, wells = None):
        if holesB is None or wells is None:
            self.reset()

    def reset(self):
        self.holesB = [[holes]*beans,[holes]*beans]
        self.wells = [0,0]

    def clone(self):
        return Kalah(holesB=deepcopy(self.holesB),
                     wells=deepcopy(self.wells))

    def __str__(self):
        return (
            "   {5:2d} {4:2d} {3:2d} {2:2d} {1:2d} {0:2d}\n".format(*self.wells[1])
        + "{0:2d}                   {1:2d}\n".format(self.holesB[1], self.holesB[0])
        + "   {0:2d} {1:2d} {2:2d} {3:2d} {4:2d} {5:2d}".format(*self.wells[0])
        )

    def is_end_pos(self):
        return not any(self.holesB[0]) and not any(self.holesB[1])

    def is_valid_move(self, move):
        h, player = move.h, move.player
        if h < 0 or h >= holes:
            return False
        beans = self.holes[player][h]
        return beans > 0

    def make_move(self, move):
        #Alter board by making move on it
        h, player = move.h, move.player
        opponent = north if player == south else south
        beans = self.holes[player][h]
        if beans == 0:
            raise ValueError("Invalid move")

        self.holes[player][h] = 0
        player_side = player
        h += 1
        while True:
