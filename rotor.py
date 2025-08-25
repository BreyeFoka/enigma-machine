import string

class Rotor:
    def __init__(self, wiring, notch):
        self.alphabet = string.ascii_uppercase
        self.wiring = wiring
        self.notch = notch
        self.position = 0

    def forward(self, char):
        index = (self.alphabet.index(char) + self.position) % 26
        return self.wiring[index]

    def backward(self, char):
        index = (self.wiring.index(char) - self.position) % 26
        return self.alphabet[index]

    def rotate(self):
        self.position = (self.position + 1) % 26
