import sys
import os
import string
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, 
    QHBoxLayout, QGridLayout, QLineEdit, QComboBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Use Wayland only when the session is Wayland; forcing it breaks X11, macOS and Windows.
if os.environ.get("WAYLAND_DISPLAY"):
    os.environ.setdefault("QT_QPA_PLATFORM", "wayland")

from enigma import REFLECTORS, ROTORS, EnigmaMachine


# UI Class
class EnigmaUI(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize Enigma machine
        rotor_configs = [ROTORS["I"], ROTORS["II"], ROTORS["III"]]
        reflector_config = REFLECTORS["B"]
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
            rotor_selector.currentIndexChanged.connect(self.update_output)

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
        """Encrypt the whole input from the chosen start positions and show it."""
        self.update_rotor_position()
        self.display_label.setText(self.enigma.encode_text(self.input_field.text()))

    def on_key_press(self, letter):
        """Handle on-screen keyboard key press."""
        current_text = self.input_field.text()
        self.input_field.setText(current_text + letter)

    def update_rotor_position(self):
        """Reset the rotors to the start positions chosen in the selectors."""
        if not hasattr(self, "rotor_positions"):
            return
        self.enigma.set_positions("".join(chr(65 + box.currentIndex()) for box in self.rotor_positions))


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EnigmaUI()
    window.show()
    sys.exit(app.exec_())
