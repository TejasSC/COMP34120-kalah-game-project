import random
from agent import Agent


class MaxMovesAgent():

    def move(self, state):
        options = Agent.valid_moves()

        current_score = state[7]

        scores = []

        for o in options:
            new_state = update_state(state, o)
            scores.append((new_state[7] - current_score, o))

        # sort the score list
        scores.sort(reverse=True)

        choose_from = []
        m = scores[0][0]
        for score in scores:
            if score[0] == m:
                choose_from.append(score[1])

        return random.choice(choose_from)