#!/usr/bin/env python3
from __init__ import *
from examples import *

import tkinter
from _tkinter import TclError

from copy import deepcopy

__all__ = []

machine = counter

game = tkinter.Tk()
game.title("Turing Machine")

table = tkinter.Label(game, text=str(machine.table), justify=tkinter.LEFT)
table.pack(side=tkinter.BOTTOM)

state_var = tkinter.StringVar(game)
state_var.set(str(machine).split("\n")[4])
state = tkinter.Entry(game, textvariable=state_var)

def check_correct() -> None:
    next(correct)
    if correct != machine:
        game.destroy()
        raise RuntimeError("That was incorrect.")


def left_arrow_callback() -> None:
    global machine
    if old_symbol := symbol_var.get():
        machine.tape[0] = old_symbol
    else:
        del machine.tape[0]
    machine.tape <<= 1
    if (new_symbol := machine.tape[0]) is not None:
        symbol_var.set(new_symbol)
    else:
        symbol_var.set("")
    check_correct()


left_arrow = tkinter.Button(game, text="←", command=left_arrow_callback)
left_arrow.pack(side=tkinter.LEFT)


def right_arrow_callback() -> None:
    global machine
    if symbol := symbol_var.get():
        machine.tape[0] = symbol
    else:
        del machine.tape[0]
    machine.tape >>= 1
    if (new_symbol := machine.tape[0]) != None:
        symbol_var.set(new_symbol)
    else:
        symbol_var.set("")
    check_correct()    


right_arrow = tkinter.Button(game, text="→", command=right_arrow_callback)
right_arrow.pack(side=tkinter.RIGHT)

symbol_var = tkinter.StringVar(game)
symbol_entry = tkinter.Entry(game, textvariable=symbol_var)

old_tape = None
next(machine)
correct = deepcopy(machine)

try:
    while True:
        game.update()
        game.update_idletasks()
        machine.state = state_var.get()
        state.pack(side=tkinter.BOTTOM)
        symbol_entry.pack(side=tkinter.BOTTOM)
        # if old_tape != (old_tape := machine.tape):
        #     print(machine.tape)
        #     print("State:\n"+machine.state)
except TclError:
    pass
