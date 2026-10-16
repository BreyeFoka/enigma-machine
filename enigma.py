from plugboard import Plugboard
from reflector import Reflector
from rotor import ALPHABET, Rotor

# Historical wirings (Enigma I / M3) and their turnover notches.
ROTORS = {
    "I": ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
    "II": ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
    "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
    "IV": ("ESOVPZJAYQUIRHXLNFTGKDCMWB", "J"),
    "V": ("VZBRGITYUPSDNHLXAWMJQOFECK", "Z"),
}
REFLECTORS = {
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMLH",
}


class EnigmaMachine:
    """A three-rotor Enigma.

    `rotors` is a list of (wiring, notch) pairs written left to right, the way
    operators wrote them (e.g. I-II-III): the last rotor is the fast one.
    """

    def __init__(self, rotors, reflector, plugboard_settings=(), positions="AAA", rings="AAA"):
        if len(rotors) != 3:
            raise ValueError("This machine takes exactly three rotors")
        self.rotors = [Rotor(wiring, notch) for wiring, notch in rotors]
        self.reflector = Reflector(reflector)
        self.plugboard = Plugboard(plugboard_settings)
        self.set_rings(rings)
        self.set_positions(positions)

    def set_positions(self, positions):
        for rotor, letter in zip(self.rotors, positions.upper()):
            rotor.position = ALPHABET.index(letter)

    def set_rings(self, rings):
        for rotor, letter in zip(self.rotors, rings.upper()):
            rotor.ring = ALPHABET.index(letter)

    def positions(self):
        return "".join(ALPHABET[r.position] for r in self.rotors)

    def step(self):
        """Advance the rotors before a key is encoded, including the double step."""
        left, middle, right = self.rotors
        if middle.at_notch():
            # The middle rotor steps itself and the left rotor (the double step).
            middle.rotate()
            left.rotate()
        elif right.at_notch():
            middle.rotate()
        right.rotate()

    def encode(self, char):
        char = char.upper()
        if char not in ALPHABET:
            raise ValueError(f"Enigma only encodes letters A-Z, got {char!r}")
        self.step()
        char = self.plugboard.substitute(char)
        for rotor in reversed(self.rotors):
            char = rotor.forward(char)
        char = self.reflector.reflect(char)
        for rotor in self.rotors:
            char = rotor.backward(char)
        return self.plugboard.substitute(char)

    def encode_text(self, text):
        """Encode the letters in `text`, skipping spaces, digits and punctuation."""
        return "".join(self.encode(c) for c in text.upper() if c in ALPHABET)
