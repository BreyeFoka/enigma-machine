import pytest

from enigma import REFLECTORS, ROTORS, EnigmaMachine


def machine(positions="AAA", rings="AAA", plugs=()):
    return EnigmaMachine(
        [ROTORS["I"], ROTORS["II"], ROTORS["III"]],
        REFLECTORS["B"],
        plugs,
        positions=positions,
        rings=rings,
    )


def test_matches_the_historical_enigma_reference():
    # Enigma I, rotors I-II-III, reflector B, rings AAA, start AAA, no plugboard.
    assert machine().encode_text("AAAAA") == "BDZGO"


def test_middle_rotor_double_steps():
    m = machine(positions="ADU")
    seen = []
    for _ in range(3):
        m.encode("A")
        seen.append(m.positions())
    # U -> V turns the middle rotor to E (its notch), which then steps
    # itself and the left rotor on the very next key.
    assert seen == ["ADV", "AEW", "BFX"]


def test_decrypting_with_the_same_settings_returns_the_message():
    settings = dict(positions="QEV", rings="BKZ", plugs=[("A", "R"), ("G", "K"), ("O", "X")])
    secret = machine(**settings).encode_text("Attack at dawn")
    assert secret != "ATTACKATDAWN"
    assert machine(**settings).encode_text(secret) == "ATTACKATDAWN"


def test_no_letter_ever_encrypts_to_itself():
    m = machine()
    for _ in range(200):
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            assert m.encode(letter) != letter


def test_ring_setting_matches_the_reference():
    # Same machine with every ring set to B.
    assert machine(rings="BBB").encode_text("AAAAA") == "EWTYX"


def test_rejects_invalid_settings():
    with pytest.raises(ValueError):
        machine(plugs=[("A", "B"), ("A", "C")])
    with pytest.raises(ValueError):
        machine().encode("1")
