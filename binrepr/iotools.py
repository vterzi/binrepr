"""
Functions for printing integers and floating-point numbers in binary
representations.
"""

__all__ = ["print_int_bin", "print_float_bin"]

from .free import n_exp_bits


def _fmt(string: str, color: int) -> str:
    """
    Add to the string `string` an ANSI escape code for the standard color with
    the number `color` (0..7).
    """
    return f"\x1b[{30 + color}m{string}\x1b[m"


def print_int_bin(b: str) -> None:
    """
    Print the binary representation `b` of an integer to the standard output.
    """
    print(_fmt(b[0], 4) + _fmt(b[1:], 1))


def print_float_bin(b: str) -> None:
    """
    Print the binary representation `b` of an floating-point number to the
    standard output.
    """
    n_exponent_bits = n_exp_bits(len(b))
    print(
        _fmt(b[0], 4)
        + _fmt(b[1 : n_exponent_bits + 1], 2)
        + _fmt(b[n_exponent_bits + 1 :], 1)
    )
