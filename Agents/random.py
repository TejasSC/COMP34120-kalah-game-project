

import random
from agent import Agent


class RandomAgent(Agent):

    def move(self, state):
        options = Agent.valid_moves()

        if len(options < 1):
            return -1

        return random.choice(options)