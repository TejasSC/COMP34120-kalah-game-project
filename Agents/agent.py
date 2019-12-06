
class Agent():
    # return an index of a chosen move
    def move(self, state):
        return NotImplementedError('Class {} does not implement move()'.format(self.__class__.__name__))

    # return a list of valid indices
    def valid_moves(self, state):
        valid = []
        for i in range(0, 8):
            if state[i] > 0:
                valid.append(i)

        return valid