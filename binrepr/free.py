"""Functions for converting basic types to their binary representations."""

__all__ = [
    "max_n_digits",
    "n_exp_bits",
    "n_significand_bits",
    "n_significand_digits",
    "exp_bias",
    "max_exp",
    "min_exp",
    "max_n_exp_digits",
    "max_uint",
    "max_int",
    "min_int",
    "max_float",
    "min_float",
    "bool2bin",
    "bin2bool",
    "char2bin",
    "bin2char",
    "uint2bin",
    "bin2uint",
    "int2bin",
    "bin2int",
    "float2bin",
    "bin2float",
]

from math import inf, nan, isinf, isnan, log10

_LOG10_2 = log10(2)
_MIN_N_BITS = 8


def _fill_bits(b: str, n_bits: int, bit: bool = False) -> str:
    """
    Fill the binary representation `b` to the length `n_bits` with bits
    corresponding to `bit`.
    """
    n_bits = n_bits - len(b)
    if n_bits < 0:
        raise ValueError("not enough bits")
    return n_bits * str(int(bit)) + b


def _dec2bin(d: int, inv: bool = False) -> str:
    """
    Convert the decimal integer `d` to its binary representation and, if `inv`
    is true, invert the bits.
    """
    b = ""
    if inv:
        true_bit = "0"
        false_bit = "1"
    else:
        true_bit = "1"
        false_bit = "0"
    while d > 0:
        b = (true_bit if d & 1 else false_bit) + b
        d >>= 1
    return b


def _bin2dec(b: str, inv: bool = False) -> int:
    """
    Convert the binary representation `b` to its decimal integer.  If `inv` is
    true, use inverted bits.
    """
    bit = "0" if inv else "1"
    i = 0
    while i < len(b) and b[i] != bit:
        i += 1
    d = 0
    pos = 1
    for c in reversed(b[i:]):
        if c == bit:
            d += pos
        pos <<= 1
    return d


def max_uint(n_bits: int) -> int:
    """Return the maximum unsigned integer of the bit size `n_bits`."""
    return 2**n_bits - 1


def max_int(n_bits: int) -> int:
    """Return the maximum signed integer of the bit size `n_bits`."""
    return max_uint(n_bits - 1)


def min_int(n_bits: int) -> int:
    """Return the minimum signed integer of the bit size `n_bits`."""
    return -max_uint(n_bits - 1) - 1


def max_n_digits(n_bits: int, signed: bool = False) -> int:
    """
    Return the maximum number of decimal digits needed to represent an integer
    of the bit size `n_bits`.  If `signed` is true, the sign bit is excluded.
    """
    if signed:
        n_bits -= 1
    return int(n_bits * _LOG10_2) + 1


def n_exp_bits(n_bits: int) -> int:
    """
    Return the number of bits needed to represent the exponent of a
    floating-point number of the bit size `n_bits`.
    """
    if n_bits < _MIN_N_BITS:
        raise ValueError("not enough bits")
    mem = 8
    n_exponent_bits = 3
    inc = 2
    inc_inc = 1
    while mem < n_bits:
        mem <<= 1
        n_exponent_bits += inc
        inc_inc += 1
        if inc == inc_inc:
            inc += 1
            inc_inc = 1
    return n_exponent_bits


def n_significand_bits(n_bits: int) -> int:
    """
    Return the number of bits needed to represent the significand of a
    floating-point number of the bit size `n_bits`.
    """
    return n_bits - n_exp_bits(n_bits)


def n_significand_digits(n_bits: int) -> float:
    """
    Return the number of decimal digits needed to represent the significand of
    a floating-point number of the bit size `n_bits`.
    """
    return n_significand_bits(n_bits) * _LOG10_2


def exp_bias(n_bits: int) -> int:
    """
    Return the exponent bias of a floating-point number of the bit size
    `n_bits`.
    """
    return max_int(n_exp_bits(n_bits))


def max_exp(n_bits: int) -> int:
    """
    Return the maximum exponent with base 2 of a floating-point number of the
    bit size `n_bits`.
    """
    return exp_bias(n_bits)


def min_exp(n_bits: int, subnorm: bool = False) -> int:
    """
    Return the minimum exponent with base 2 of a floating-point number of the
    bit size `n_bits`.  If `subnorm` is true, subnormal numbers are included.
    """
    return (
        -exp_bias(n_bits)
        + 1
        - (n_significand_bits(n_bits) - 1 if subnorm else 0)
    )


def max_n_exp_digits(n_bits: int) -> int:
    """
    Return the maximum number of decimal digits needed to represent the
    exponent of a floating-point number of the bit size `n_bits`.
    """
    return int(log10(-min_exp(n_bits, subnorm=True) * _LOG10_2)) + 1


def max_float(n_bits: int) -> float:
    """
    Return the largest positive floating-point number of the bit size `n_bits`.
    """
    n = n_significand_bits(n_bits)
    return float((2**n - 1) * 2 ** (max_exp(n_bits) - n + 1))


def min_float(n_bits: int, subnorm: bool = False) -> float:
    """
    Return the smallest positive floating-point number of the bit size
    `n_bits`.
    """
    return 2 ** min_exp(n_bits, subnorm=subnorm)


def bool2bin(b: bool, n_bits: int) -> str:
    """
    Convert the Boolean `b` to its binary representation of the length
    `n_bits`.
    """
    return _fill_bits("1" if b else "0", n_bits)


def bin2bool(b: str) -> bool:
    """Convert the binary representation `b` to its Boolean."""
    return "1" in b


def char2bin(c: str) -> str:
    """Convert the character `c` to its binary representation."""
    i = ord(c)
    return _fill_bits(_dec2bin(i), 8 if i < 256 else 32)


def bin2char(b: str) -> str:
    """Convert the binary representation `b` to its character."""
    return chr(_bin2dec(b))


def uint2bin(i: int, n_bits: int) -> str:
    """
    Convert the unsigned integer `i` to its binary representation of the length
    `n_bits`.
    """
    if i < 0:
        raise ValueError("unsigned integer expected")
    return _fill_bits(_dec2bin(i), n_bits)


def bin2uint(b: str) -> int:
    """Convert the binary representation `b` to its unsigned integer."""
    return _bin2dec(b)


def int2bin(i: int, n_bits: int) -> str:
    """
    Convert the signed integer `i` to its binary representation of the length
    `n_bits`.
    """
    inv = i < 0
    if inv:
        sign = "1"
        i = -i - 1
    else:
        sign = "0"
    return sign + _fill_bits(_dec2bin(i, inv), n_bits - 1, inv)


def bin2int(b: str) -> int:
    """Convert the binary representation `b` to its signed integer."""
    sign = b[0]
    inv = sign == "1"
    i = _bin2dec(b[1:], inv)
    return -i - 1 if inv else i


def float2bin(f: float, n_bits: int) -> str:
    """
    Convert the floating-point number `f` to its binary representation of the
    length `n_bits`.
    """
    n_exponent_bits = n_exp_bits(n_bits)
    if isnan(f):
        return "0" + (n_bits - 1) * "1"
    if f == 0:
        return n_bits * "0"
    n_mantissa_bits = n_bits - n_exponent_bits - 1
    if f < 0:
        sign = "1"
        f = -f
    else:
        sign = "0"
    max_exponent = (1 << n_exponent_bits) - 1
    exponent = max_exponent >> 1
    if not isinf(f):
        while f < 1:
            f *= 2
            exponent -= 1
        while f >= 2:
            f *= 0.5
            exponent += 1
    else:
        exponent = max_exponent
    if exponent >= max_exponent:
        return sign + n_exponent_bits * "1" + n_mantissa_bits * "0"
    mantissa = ""
    precision = n_mantissa_bits
    if exponent <= 0:
        precision += exponent - 1
        exponent = 0
        if precision >= 0:
            mantissa += "1"
    # subtracting leading 1 and adding the smallest bit to round the value
    f += 0.5 ** (n_mantissa_bits + 1) - 1
    for _ in range(precision):
        f *= 2
        if f >= 1:
            f -= 1
            mantissa += "1"
        else:
            mantissa += "0"
    return (
        sign
        + _fill_bits(_dec2bin(exponent), n_exponent_bits)
        + _fill_bits(mantissa, n_mantissa_bits)
    )


def bin2float(b: str) -> float:
    """Convert the binary representation `b` to its floating-point number."""
    n_exponent_bits = n_exp_bits(len(b))
    sign = b[0]
    exponent = b[1 : n_exponent_bits + 1]
    mantissa = b[n_exponent_bits + 1 :]
    if "0" in exponent:
        dec_exponent = _bin2dec(exponent)
        pos = 2 ** (dec_exponent + 1 - (1 << n_exponent_bits - 1))
        if dec_exponent > 0:
            f = pos
        else:
            f = 0
            pos *= 2
        for bit in mantissa:
            pos *= 0.5
            if bit == "1":
                f += pos
    else:
        f = inf if "1" not in mantissa else nan
    return f if sign == "0" else -f
