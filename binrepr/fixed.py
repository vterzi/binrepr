"""
Functions for converting basic types to their binary representations of fixed
length (8, 16, 32, 64) in big-endian byte order.
"""

__all__ = [
    "pad2bin8",
    "byte2bin8",
    "bool2bin8",
    "int2bin8",
    "uint2bin8",
    "int2bin16",
    "uint2bin16",
    "int2bin32",
    "uint2bin32",
    "int2bin64",
    "uint2bin64",
    "float2bin16",
    "float2bin32",
    "float2bin64",
]

import struct
from typing import Any

_BYTE_ORDERS = {
    "default": "@",
    "native": "=",
    "little-endian": "<",
    "big-endian": ">",
    "network": "!",
}
_BYTE_ORDER = _BYTE_ORDERS["big-endian"]


def _val2bin(x: Any, fmt: str) -> str:
    """
    Convert the value `x` to its binary representation using the format
    character `fmt`.
    """
    return "".join(f"{b:0>8b}" for b in struct.pack(_BYTE_ORDER + fmt, x))


def pad2bin8() -> str:
    """Convert the pad byte to its 8-bit binary representation."""
    return "".join(f"{b:0>8b}" for b in struct.pack(_BYTE_ORDER + "x"))


def byte2bin8(b: bytes) -> str:
    """Convert the byte `b` to its 8-bit binary representation."""
    return _val2bin(b, "c")


def bool2bin8(b: bool) -> str:
    """Convert the Boolean `b` to its 8-bit binary representation."""
    return _val2bin(b, "?")


def int2bin8(i: int) -> str:
    """Convert the signed integer `i` to its 8-bit binary representation."""
    return _val2bin(i, "b")


def uint2bin8(i: int) -> str:
    """Convert the unsigned integer `i` to its 8-bit binary representation."""
    return _val2bin(i, "B")


def int2bin16(i: int) -> str:
    """Convert the signed integer `i` to its 16-bit binary representation."""
    return _val2bin(i, "h")


def uint2bin16(i: int) -> str:
    """Convert the unsigned integer `i` to its 16-bit binary representation."""
    return _val2bin(i, "H")


def int2bin32(i: int) -> str:
    """Convert the signed integer `i` to its 32-bit binary representation."""
    return _val2bin(i, "l")


def uint2bin32(i: int) -> str:
    """Convert the unsigned integer `i` to its 32-bit binary representation."""
    return _val2bin(i, "L")


def int2bin64(i: int) -> str:
    """Convert the signed integer `i` to its 64-bit binary representation."""
    return _val2bin(i, "q")


def uint2bin64(i: int) -> str:
    """Convert the unsigned integer `i` to its 64-bit binary representation."""
    return _val2bin(i, "Q")


def float2bin16(f: float) -> str:
    """
    Convert the floating-point number `f` to its 16-bit binary representation.
    """
    return _val2bin(f, "e")


def float2bin32(f: float) -> str:
    """
    Convert the floating-point number `f` to its 32-bit binary representation.
    """
    return _val2bin(f, "f")


def float2bin64(f: float) -> str:
    """
    Convert the floating-point number `f` to its 64-bit binary representation.
    """
    return _val2bin(f, "d")
