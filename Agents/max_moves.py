import random
from agent import Agent


class MaxScoreAgent():

    def move(self, state):
        options = Agent.valid_moves()

        additional_move = []

        for o in options:
            seeds = state[o]

            if (o + seeds) % 15 == 7:
                additional_move.append(o)


        if not additional_move:
            return random.choice(options)

        return random.choice(additional_move)