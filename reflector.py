import string

ALPHABET = string.ascii_uppercase


class Reflector:
    def __init__(self, wiring):
        for i, letter in enumerate(ALPHABET):
            partner = wiring[i]
            if partner == letter or wiring[ALPHABET.index(partner)] != letter:
                raise ValueError("Reflector wiring must pair every letter with a different one")
        self.wiring = wiring

    def reflect(self, char):
        return self.wiring[ALPHABET.index(char)]
