import string

class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring
        self.alphabet = string.ascii_uppercase

    def reflect(self, char):
        index = self.alphabet.index(char)
        return self.wiring[index]
