#!/usr/bin/env python3
# Copyright (c) 2016-2020, henry232323
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from random import sample

_wdalpha = {
        "!": 9999, "\"": 9986, "#": 9985, "$": 128083, "%": 128365,
        "&": 128366, "'": 128367, "(": 9742, ")": 9990, "*": 128386,
        "+": 128387, ",": 128234, "-": 128235, ".": 128236, "/": 128237,
        "0": 128193, "1": 128194, "2": 128196, "3": 128463, "4": 128464,
        "5": 128452, "6": 8987, "7": 128430, "8": 128432, "9": 128434,
        ":": 128435, ";": 128436, "<": 128427, "=": 128428, ">": 9991,
        "?": 9997, "@": 128398, "A": 9996, "B": 128076, "C": 128077,
        "D": 128078, "E": 9756, "F": 9758, "G": 9757, "H": 9759,
        "I": 9995, "J": 9786, "K": 128528, "L": 9785, "M": 128163,
        "N": 9760, "O": 9872, "P": 127985, "Q": 9992, "R": 9788,
        "S": 128167, "T": 10052, "U": 128326, "V": 10014, "W": 128328,
        "X": 10016, "Y": 10017, "Z": 9770, "[": 9775, "\\": 2384,
        "]": 9784, "^": 9800, "_": 9801, "`": 9802, "{": 10048,
        "|": 10047, "}": 10077, "~": 10078, "a": 9803, "b": 9804,
        "c": 9805, "d": 9806, "e": 9807, "f": 9808, "g": 9809,
        "h": 9810, "i": 9811, "k": 38, "l": 9679, "m": 10061,
        "n": 9632, "o": 9633, "q": 10065, "r": 10066, "s": 11047,
        "t": 10731, "u": 9670, "v": 10070, "w": 11045, "x": 8999,
        "y": 9043, "z": 8984, "p": 128912, "j": 128624
    }

def lower(str):
    return str.lower()


def reverse(str):
    return reverse(str)


def upper(str):
    return str.upper()


def scramble(text):
    return "".join(sample(text, len(text)))


def capitalize(str):
    return str.capitalize()


def wingding(str):
    f = ""
    for char in str:
        try:
            char = chr(_wdalpha[char])
        except KeyError:
            pass
        f += char
    return f