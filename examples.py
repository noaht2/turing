#!/usr/bin/env python3
from __init__ import *
from time import sleep

__all__ = ["right_then_left", "counter", "flipping_cards"]

right_then_left = Machine(
    Tape(neg=["r"], mid=None, pos=["l"]),
    "R",
    Table(
        {
            "R": {
                None: (None, "R", Tape.irshift),
                "l": ("l", "L", Tape.ilshift)
            },
            "L": {
                None: (None, "L", Tape.ilshift),
                "r": ("r", "R", Tape.irshift)
            }
        }
    )
)

counter = Machine(
    Tape(neg=["1", "0", "1"], mid="1", pos=[]),
    "0",
    Table(
        {
            "0": {
                "1": ("1", "0", Tape.irshift),
                "0": ("0", "0", Tape.irshift),
                None: (None, "1", Tape.ilshift)
            },
            "1": {
                "0": ("1", "0", Tape.irshift),
                "1": ("0", "1", Tape.ilshift),
                None: ("1", "0", Tape.irshift)
            }
        }
    )
)

flipping_cards = Machine(
    Tape(neg=[], mid="d", pos=["d"]*6),
    "engaged",
    Table(
        {
            "engaged": {
                "d": ("u", "reset", Tape.ilshift),
                "u": ("d", "engaged", Tape.irshift),
                None: (None, "reset", Tape.ilshift)
            },
            "reset": {
                "d": ("d", "reset", Tape.ilshift),
                "u": ("u", "reset", Tape.ilshift),
                None: (None, "engaged", Tape.irshift)
            }
        }
    )
)

if __name__ == "__main__":
    i = 0
    for cycle in flipping_cards:
        print(cycle)
        if len(cycle.neg) == 0:
            i += 1
        if all([x == "u" or x is None for x in cycle.neg+[cycle.mid]+cycle.pos]):
            print(i)
            break
