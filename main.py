import tkinter as tk
from enigma import EnigmaMachine

# Initialize the Enigma machine with configurations
rotor_configs = [
    ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),  # Rotor I
    ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),  # Rotor II
    ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),  # Rotor III
]
reflector_config = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
plugboard_settings = [("A", "B"), ("C", "D")]

enigma = EnigmaMachine(rotor_configs, reflector_config, plugboard_settings)

# GUI Setup
def create_gui():
    root = tk.Tk()
    root.title("Enigma Machine")

    # Create the keyboard
    def on_key_press(char):
        output = enigma.encode(char)
        output_label.config(text=output)

    keyboard_frame = tk.Frame(root)
    keyboard_frame.pack()

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        button = tk.Button(keyboard_frame, text=letter, command=lambda l=letter: on_key_press(l))
        button.pack(side=tk.LEFT)

    # Output display
    output_label = tk.Label(root, text="", font=("Arial", 24))
    output_label.pack()

    root.mainloop()

create_gui()
