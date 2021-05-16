#!/usr/bin/env python3
import collections.abc
from numbers import Integral
from copy import deepcopy
from enum import Enum

__all__ = ["Tape", "Table", "Machine"]


def _unlist(seq: collections.abc.Iterable) -> str:
    return "|".join(map((lambda x: repr(x) if x is not None else "' '"), seq))


def _enough_before(seq: list, index: Integral):
    try:
        return seq[:index]
    except IndexError:
        return _enough_before(seq+[None], index)


def _enough_after(seq: list, index: Integral):
    try:
        return seq[index:]
    except IndexError:
        return _enough_before([None]+seq, index)


class Tape:
    def __init__(self, neg: list = [], neg_beyond=None, mid=None, pos: list = [], pos_beyond=None):
        self.neg = neg
        self.neg_beyond = neg_beyond
        self.mid = mid
        self.pos = pos
        self.pos_beyond = pos_beyond

    def __str__(self):
        headpos = len(self.neg)+1
        output = " "*(headpos*4-1)+"↓"
        output += "\n |"+_unlist(self.neg[::-1]+[self.mid]+self.pos)+"|"
        return output

    def __repr__(self):
        return (
            "Tape("
            + repr(self.neg)+", "
            + repr(self.neg_beyond)+", "
            + repr(self.mid)+", "
            + repr(self.pos)+", "
            + repr(self.pos_beyond)
            + ")"
        )

    def __getitem__(self, key):
        if key < 0:
            try:
                return self.neg[-key-1]
            except IndexError:
                return self.neg_beyond
        elif key == 0:
            return self.mid
        elif key > 0:
            try:
                return self.pos[key-1]
            except IndexError:
                return self.pos_beyond

    def __setitem__(self, key, value):
        if key < 0:
            if -key > len(self.neg):
                self.neg += [self.neg_beyond]*-key-len(self.neg)
            self.neg[-key-1] = value
        elif key == 0:
            self.mid = value
        elif key > 0:
            if key > len(self.neg):
                self.pos += [self.pos_beyond]*(len(self.pos)-key)
            self.pos[key-1] = value

    def __delitem__(self, key):
        self[key] = None

    def ilshift(self, amount: int = 1) -> None:
        for i in range(amount):
            self.pos.insert(0, self.mid)
            if len(self.neg) > 0:
                self[0] = self.neg.pop(0)
            else:
                self[0] = self.neg_beyond

    def __lshift__(self, amount):
        new = deepcopy(self)
        new.ilshift(amount)
        return new

    def irshift(self, amount: int = 1) -> None:
        for i in range(amount):
            self.neg.insert(0, self.mid)
            if len(self.pos) > 0:
                self[0] = self.pos.pop(0)
            else:
                self[0] = self.pos_beyond

    def __rshift__(self, amount):
        new = deepcopy(self)
        new.irshift(amount)
        return new

    def __eq__(self, other):
        return (self.neg, self.neg_beyond. self.mid, self.pos, self.pos_beyond) == (other.neg, other.neg_beyond, other.mid, other.pos, other.pos_beyond)


class Table(dict):
    def __repr__(self):
        return "Table({})".format(super().__repr__())

    def __str__(self):
        output = ""
        for state in self:
            output += "if state is \"{}\",".format(state)
            for symbol in self[state]:
                if symbol is None:
                    output += "\n    if symbol is blank,"
                else:
                    output += "\n    if symbol is \"{}\",".format(symbol)
                new_symbol, new_state, movement = self[state][symbol]
                if new_symbol is None:
                    output += "\n        write a blank;"
                else:
                    output += "\n        write \"{}\";".format(new_symbol)
                output += "\n        make state \"{}\";".format(new_state)
                if movement is Tape.ilshift:
                    output += "\n        move left,"
                elif movement is Tape.irshift:
                    output += "\n        move right,"
                elif movement is None:
                    output += "\n        stay still,"
            output += "\n"
        return output


class Machine:
    def __init__(self, tape: Tape, state: str, table: Table):
        self.tape = tape
        self.state = state
        self.table = table

    def __str__(self):
        return (
            "Tape:\n"+str(self.tape)+"\nState:\n"+str(self.state)
            + "\nTable:\n"+str(self.table)
        )

    def __repr__(self):
        return (
            "Machine("+repr(self.tape)+", "+repr(self.state)+", "
            + repr(self.table)+")"
        )

    def __iter__(self):
        return self

    def __next__(self):
        instructions = self.table[self.state][self.tape[0]]
        symbol, state, movement = instructions
        self.tape[0] = symbol
        if movement is Tape.ilshift:
            self.tape <<= 1
        elif movement is Tape.irshift:
            self.tape >>= 1
        elif movement is None:
            pass
        self.state = state
        return self.tape

    def __eq__(self, other):
        return (self.tape, self.state, self.table) == (other.tape, other.state, other.table)
