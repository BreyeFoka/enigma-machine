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
    root.geometry("600x400")  # Set window size

    # Input and Output Text Boxes
    input_text = tk.StringVar()
    output_text = tk.StringVar()

    def update_output():
        """Update the output text based on the input."""
        word = input_text.get().upper()
        ciphered = ''.join(enigma.encode(char) for char in word if char.isalpha())
        output_text.set(ciphered)

    input_label = tk.Label(root, text="Input:")
    input_label.pack(anchor=tk.W, padx=10)
    
    input_entry = tk.Entry(root, textvariable=input_text, font=("Arial", 14), width=50)
    input_entry.pack(pady=10, padx=10)

    output_label = tk.Label(root, text="Ciphered:")
    output_label.pack(anchor=tk.W, padx=10)

    output_display = tk.Entry(root, textvariable=output_text, font=("Arial", 14), width=50, state='readonly')
    output_display.pack(pady=10, padx=10)

    # Keyboard Handling
    def on_key_press(event):
        """Handle keyboard key presses."""
        char = event.char.upper()
        if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            input_text.set(input_text.get() + char)
            update_output()
            return "break"  # Prevent default handling

    # Ensure `on_key_press` is bound only once
    if not hasattr(root, "_key_press_bound"):
        root.bind("<KeyPress>", on_key_press)
        root._key_press_bound = True  # Track the binding to prevent duplicates

    # On-Screen Keyboard
    def on_screen_key_press(char):
        """Handle on-screen keyboard presses."""
        input_text.set(input_text.get() + char)
        update_output()

    keyboard_frame = tk.Frame(root)
    keyboard_frame.pack(side=tk.BOTTOM, pady=20)

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        button = tk.Button(
            keyboard_frame, 
            text=letter, 
            width=4, 
            height=2, 
            command=lambda l=letter: on_screen_key_press(l)
        )
        button.grid(row=(ord(letter) - ord('A')) // 10, column=(ord(letter) - ord('A')) % 10, padx=5, pady=5)

    root.mainloop()

create_gui()
