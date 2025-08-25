import sys
import os
import string
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, 
    QHBoxLayout, QGridLayout, QLineEdit, QComboBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Set the QT_QPA_PLATFORM environment variable to xcb
os.environ["QT_QPA_PLATFORM"] = "xcb"

# Import the logic classes
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


class Plugboard:
    def __init__(self, settings):
        self.mapping = {char: char for char in string.ascii_uppercase}
        for pair in settings:
            a, b = pair
            self.mapping[a], self.mapping[b] = b, a

    def substitute(self, char):
        return self.mapping[char]


class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring
        self.alphabet = string.ascii_uppercase

    def reflect(self, char):
        index = self.alphabet.index(char)
        return self.wiring[index]


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


# UI Class
class EnigmaUI(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize Enigma machine
        rotor_configs = [
            ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),  # Rotor I
            ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),  # Rotor II
            ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),  # Rotor III
        ]
        reflector_config = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
        plugboard_settings = [("A", "B"), ("C", "D")]
        self.enigma = EnigmaMachine(rotor_configs, reflector_config, plugboard_settings)

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Enigma Machine")
        self.setGeometry(100, 100, 900, 600)
        
        main_layout = QVBoxLayout()

        # Display label
        self.display_label = QLabel("Output", self)
        self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setFont(QFont("Courier", 20))
        main_layout.addWidget(self.display_label)

        # Input field
        self.input_field = QLineEdit(self)
        self.input_field.setFont(QFont("Courier", 16))
        self.input_field.textChanged.connect(self.update_output)
        main_layout.addWidget(self.input_field)

        # Rotor Selection
        rotor_layout = QHBoxLayout()
        self.rotor_positions = []
        for i in range(3):
            rotor_label = QLabel(f"Rotor {i+1}", self)
            rotor_label.setFont(QFont("Arial", 12))

            rotor_selector = QComboBox(self)
            rotor_selector.addItems([chr(x) for x in range(65, 91)])  # A-Z
            rotor_selector.currentIndexChanged.connect(self.update_rotor_position)

            self.rotor_positions.append(rotor_selector)
            rotor_layout.addWidget(rotor_label)
            rotor_layout.addWidget(rotor_selector)

        main_layout.addLayout(rotor_layout)

        # Plugboard section
        plugboard_label = QLabel("Plugboard", self)
        plugboard_label.setFont(QFont("Arial", 14))
        plugboard_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(plugboard_label)

        # Keyboard grid
        keyboard_layout = QGridLayout()
        self.keyboard_buttons = {}
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, letter in enumerate(letters):
            btn = QPushButton(letter, self)
            btn.setFont(QFont("Arial", 12))
            btn.setFixedSize(50, 50)
            btn.clicked.connect(lambda _, l=letter: self.on_key_press(l))
            keyboard_layout.addWidget(btn, i // 10, i % 10)
            self.keyboard_buttons[letter] = btn

        main_layout.addLayout(keyboard_layout)

        # Encode Button
        self.encode_button = QPushButton("Encode", self)
        self.encode_button.setFont(QFont("Arial", 14))
        self.encode_button.clicked.connect(self.update_output)
        main_layout.addWidget(self.encode_button)

        self.setLayout(main_layout)

    def update_output(self):
        """Encrypt the input text and update the output display."""
        word = self.input_field.text().upper()
        ciphered = ''.join(self.enigma.encode(char) for char in word if char.isalpha())
        self.display_label.setText(ciphered)

    def on_key_press(self, letter):
        """Handle on-screen keyboard key press."""
        current_text = self.input_field.text()
        self.input_field.setText(current_text + letter)

    def update_rotor_position(self):
        """Update rotor positions based on user selection."""
        for i, rotor in enumerate(self.rotor_positions):
            self.enigma.rotors[i].position = rotor.currentIndex()


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EnigmaUI()
    window.show()
    sys.exit(app.exec_())
