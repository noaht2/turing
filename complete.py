#!/usr/bin/env python3

from typing import *
from itertools import cycle
import sys

from __init__ import *

STATES = ["1", "2", "3", "4", "5", "6", "7", "8",
          "9", "10", "11", "12", "13", "14", "15"]

universal = Table({"1":
                   {"0":
                    ("0", "2", Tape.irshift),
                    "1":
                    ("1", "1", Tape.irshift)},
                   "2":
                   {"0":
                    ("1", "3", Tape.irshift),
                    "1":
                    ("1", "1", Tape.irshift)},
                   "3":
                   {"0":
                    ("0", "7", Tape.ilshift),
                    "1":
                    ("0", "5", Tape.ilshift)},
                   "4":
                   {"0":
                    ("0", "6", Tape.ilshift),
                    "1":
                    ("1", "5", Tape.ilshift)},
                   "5":
                   {"0":
                    ("1", "1", Tape.irshift),
                    "1":
                    ("1", "4", Tape.ilshift)},
                   "6":
                   {"0":
                    ("1", "4", Tape.ilshift),
                    "1":
                    ("1", "4", Tape.ilshift)},
                   "7":
                   {"0":
                    ("0", "8", Tape.ilshift),
                    "1":
                    ("1", "7", Tape.ilshift)},
                   "8":
                   {"0":
                    ("1", "9", Tape.ilshift),
                    "1":
                    ("1", "7", Tape.ilshift)},
                   "9":
                   {"0":
                    ("0", "1", Tape.irshift),
                    "1":
                    ("1", "10", Tape.ilshift)},
                   "10":
                   {"0":
                    ("1", "11", Tape.ilshift),
                    "1":
                    ("1", "1", None)},  # Irrelevant?
                   "11":
                   {"0":
                    ("0", "12", Tape.irshift),
                    "1":
                    ("1", "14", Tape.irshift)},
                   "12":
                   {"0":
                    ("0", "13", Tape.irshift),
                    "1":
                    ("1", "12", Tape.irshift)},
                   "13":
                   {"0":
                    ("0", "2", Tape.ilshift),
                    "1":
                    ("1", "12", Tape.irshift)},
                   "14":
                   {"0":
                    ("0", "3", Tape.ilshift),
                    "1":
                    ("0", "15", Tape.irshift)},
                   "15":
                   {"0":
                    ("0", "14", Tape.irshift),
                    "1":
                    ("1", "14", Tape.irshift)}})


def alternate():
    while True:
        yield "0"
        yield "1"


def side():
    i = 0
    while True:
        yield list(bin(i))[2:]
        i += 1


class LazyList:
    def __init__(self, iterator: Iterator[Any]):
        self._iterator = iterator
        self._list = []

    def __getitem__(self, key):
        if key >= len(self._list):
            for _ in range(key - len(self._list) + 1):
                self._list.append(next(self._iterator))
        return self._list[key]

        
def intermingle(g1, g2):
    s1, s2 = LazyList(g1), LazyList(g2)
    i, j = 0, 0
    while True:
        while i != 0:
            i -= 1
            j += 1
            yield s1[i], s2[j]
        j += 1
        while j != 0:
            i += 1
            j -= 1
            yield s1[i], s2[j]
        i += 1


def tapes():
    for (((neg, neg_beyond), (pos, pos_beyond)), mid) in intermingle(intermingle(intermingle(side(), alternate()), intermingle(side(), alternate())), alternate()):
        yield Tape(neg=neg, neg_beyond=neg_beyond, mid=mid, pos=pos, pos_beyond=pos_beyond)

                
def machines():
    for tape in tapes():
        for state in STATES:
            yield Machine(tape, state, universal)


if __name__ == "__main__":
    tms = []
    for machine in machines():
        tms.append(machine)
        for i in range(len(tms)):
            try:
                next(tms[i])
            except KeyboardInterrupt:
                print(len(tms))
                sys.exit()
