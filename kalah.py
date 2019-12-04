from copy import deepcopy

SOUTH = 0
NORTH = 1
holes = 7
hole_beans = 7


class Game(object):
    def __init__(self, holes=None, scoring_wells=None):
        if holes is None or scoring_wells is None:
            self.restart()
        else:
            self.holes = holes
            self.scoring_wells = scoring_wells

    def restart(self):
        self.holes = [
            [hole_beans] * holes,
            [hole_beans] * holes,
        ]
        self.scoring_wells = [0, 0]

    def clone(self):
        return Game(holes=deepcopy(self.holes),
                     scoring_wells=deepcopy(self.scoring_wells))

    def is_end_pos(self):
        return not any(self.holes[0]) and not any(self.holes[1])

    def move_is_legal(self, move):
        hole = move.hole
        player = move.player
        if hole < 0 or hole >= holes:
            return False
        beans = self.holes[player][hole]
        return beans > 0

    def do_move(self, move):
        """
        Changing the game by making a move
        Return index of the player to make the next move
        """
        hole, player = move.hole, move.player
        opponent = NORTH if player == SOUTH else SOUTH
        beans = self.holes[player][hole]
        if beans == 0:
            raise ValueError("Invalid move")

        self.holes[player][hole] = 0
        player_side = player
        hole += 1
        while True:
            if hole >= holes:
                # Inside kalaha
                if player_side == player:
                    # Own kalaha - sow
                    self.scoring_wells[player] += 1
                    beans -= 1
                    if not beans:
                        # Turn ended inside own kalaha => new turn for player
                        # or victory if no more moves left
                        if not any(self.holes[player]):
                            for i in range(holes):
                                if self.holes[opponent][i]:
                                    self.scoring_wells[player] += self.holes[opponent][i]
                                    self.holes[opponent][i] = 0
                        return player
                hole = 0
                player_side = NORTH if player_side == SOUTH else SOUTH
            else:
                # Inside hole
                beans -= 1
                self.holes[player_side][hole] += 1
                if not beans:
                    # Turn ended
                    if player_side == player and self.holes[player][hole] == 1:
                        # Ended in own, empty hole
                        opposite_hole = holes - hole - 1
                        self.scoring_wells[player] += (self.holes[player][hole]
                                                 + self.holes[opponent][opposite_hole])
                        self.holes[player][hole] = self.holes[opponent][opposite_hole] = 0
                    # Game ended - opponent wins?
                    if not any(self.holes[opponent]):
                        for i in range(holes):
                            if self.holes[player][i]:
                                self.scoring_wells[opponent] += self.holes[player][i]
                                self.holes[player][i] = 0
                                self._anim_frame()
                    return opponent
                hole += 1


class Move(object):
    def __init__(self, hole, player):
        self.hole = hole
        self.player = player
