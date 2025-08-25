import string

class Plugboard:
    def __init__(self, settings):
        self.mapping = {char: char for char in string.ascii_uppercase}
        for pair in settings:
            a, b = pair
            self.mapping[a], self.mapping[b] = b, a

    def substitute(self, char):
        return self.mapping[char]
