import string

ALPHABET = string.ascii_uppercase


class Plugboard:
    def __init__(self, settings):
        self.mapping = {char: char for char in ALPHABET}
        used = set()
        for a, b in settings:
            a, b = a.upper(), b.upper()
            if a == b or a in used or b in used:
                raise ValueError(f"Invalid plugboard pair {a}{b}: each letter can be plugged once")
            used.update((a, b))
            self.mapping[a], self.mapping[b] = b, a

    def substitute(self, char):
        return self.mapping[char]
