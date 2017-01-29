from random import sample

def lower(str):
    return str.lower()


def reverse(str):
    return reverse(str)


def upper(str):
    return str.upper()


def scramblerep(text):
    return "".join(sample(text, len(text)))
