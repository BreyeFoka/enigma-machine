from rotor import Rotor
from reflector import Reflector
from plugboard import Plugboard

class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard_settings):
        self.rotors = [Rotor(wiring, notch) for wiring, notch in rotors]
        self.reflector = Reflector(reflector)
        self.plugboard = Plugboard(plugboard_settings)

    def encode(self, char):
        char = self.plugboard.substitute(char)
        for rotor in self.rotors:
            char = rotor.forward(char)
        char = self.reflector.reflect(char)
        for rotor in reversed(self.rotors):
            char = rotor.backward(char)
        char = self.plugboard.substitute(char)
        self.rotors[0].rotate()
        return char
