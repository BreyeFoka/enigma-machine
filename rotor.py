import string

ALPHABET = string.ascii_uppercase


class Rotor:
    """One Enigma rotor.

    `position` is the letter showing in the window (0 = A) and `ring` the ring
    setting (Ringstellung, 0 = A). Both shift the signal on the way in and back
    out again, which is what makes the same wiring produce a different
    substitution at every position.
    """

    def __init__(self, wiring, notch, position=0, ring=0):
        if sorted(wiring) != list(ALPHABET):
            raise ValueError("Rotor wiring must use each letter A-Z exactly once")
        self.wiring = wiring
        self.notch = notch
        self.position = position % 26
        self.ring = ring % 26

    def _shift(self):
        return self.position - self.ring

    def forward(self, char):
        """Right-to-left pass, towards the reflector."""
        shift = self._shift()
        contact = (ALPHABET.index(char) + shift) % 26
        out = ALPHABET.index(self.wiring[contact])
        return ALPHABET[(out - shift) % 26]

    def backward(self, char):
        """Left-to-right pass, back from the reflector."""
        shift = self._shift()
        contact = (ALPHABET.index(char) + shift) % 26
        out = self.wiring.index(ALPHABET[contact])
        return ALPHABET[(out - shift) % 26]

    def at_notch(self):
        return ALPHABET[self.position] in self.notch

    def rotate(self):
        self.position = (self.position + 1) % 26
