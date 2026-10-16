# Enigma machine

A simulator of the three-rotor Enigma I used by the German army in the Second World War, with a PyQt5 interface. Messages it encrypts can be decrypted by any accurate Enigma simulator with the same settings.

## How it works

Each key press:

1. **Steps the rotors** before the letter is encoded. The right rotor always steps; at its notch it turns the middle rotor, and the middle rotor at its own notch steps itself and the left rotor too (the double step).
2. Sends the letter through the **plugboard**, the three rotors right to left, the **reflector**, then back through the rotors left to right and the plugboard again.

Each rotor's position and ring setting shift the signal on the way in and on the way out, so the same wiring gives a different substitution at every position. Because of the reflector, the machine is its own inverse (the same settings decrypt), and no letter ever encrypts to itself.

Included: rotors I to V and reflectors B and C, with their historical wirings and notches.

## Use it

```bash
pip install -r requirements.txt
python main.py            # the GUI: pick start positions and type
```

```python
from enigma import EnigmaMachine, ROTORS, REFLECTORS

m = EnigmaMachine([ROTORS["I"], ROTORS["II"], ROTORS["III"]], REFLECTORS["B"],
                  plugboard_settings=[("A", "R"), ("G", "K")], positions="QEV", rings="BKZ")
secret = m.encode_text("Attack at dawn")
```

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

The tests check the standard reference results (rotors I-II-III, reflector B, start AAA: `AAAAA` encrypts to `BDZGO`; with rings BBB, to `EWTYX`), the double step, decryption with the same settings and that no letter maps to itself. GitHub Actions runs them on every push.

## Limitations

- Three-rotor machine only: no four-rotor naval M4 and no thin reflectors.
- The plugboard pairs are set in code (`main.py`); the interface doesn't edit them yet.
