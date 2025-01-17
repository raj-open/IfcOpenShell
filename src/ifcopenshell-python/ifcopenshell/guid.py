# IfcOpenShell - IFC toolkit and geometry engine
# Copyright (C) 2021 Thomas Krijnen <thomas@aecgeeks.com>
#
# This file is part of IfcOpenShell.
#
# IfcOpenShell is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IfcOpenShell is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with IfcOpenShell.  If not, see <http://www.gnu.org/licenses/>.

"""
Reads and writes encoded GlobalIds

IFC entities may be identified using a unique ID (called a UUID or GUID). This
128-bit label is often represented in the form
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx. However, in IFC, it is also usually
stored as a 22 character base 64 encoded string. This module lets you convert
between these representations and generate new UUIDs.
"""

# ----------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------

from uuid import uuid4
import string

from functools import reduce

# ----------------------------------------------------------------
# EXPORTS
# ----------------------------------------------------------------

__all__ = [
    "compress",
    "expand",
    "split",
    "new",
]

# ----------------------------------------------------------------
# LOCAL CONSTANTS, VARIABLES
# ----------------------------------------------------------------

CHARS64 = string.ascii_uppercase + string.ascii_lowercase + string.digits + "_$"

# ----------------------------------------------------------------
# PUBLIC METHODS
# ----------------------------------------------------------------


def compress(uuid: str, /) -> str:
    """
    Converts a hex-encoded encoded GUID
    to a base64-encoded UUID.
    """
    n = len(uuid)
    L_hex = n % 6
    guid = ""

    while len(uuid) > 0:
        block, uuid = uuid[:L_hex], uuid[L_hex:]
        num = int(block, 16)
        L_64 = 4 * (L_hex // 6)
        guid += int_to_repr(num, padding=L_64)
        L_hex = 6

    return guid


def expand(guid: str, /) -> str:
    """
    Converts a base64-encoded GUID
    to a hex-encoded UUID.
    """
    n = len(guid)
    L_64 = n % 4
    uuid = ""

    while len(guid) > 0:
        block, guid = guid[:L_64], guid[L_64:]
        L_hex = 6 * (L_64 // 4)
        uuid += f"{repr_to_int(block):0{L_hex}x}"
        L_64 = 4

    return uuid


def split(uuid: str, /) -> str:
    """
    Formats a 32-character hex-encoded UUID as
    ```
    xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    ```
    """
    return "-".join([
        uuid[:8],
        uuid[8:][:4],
        uuid[12:][:4],
        uuid[16:][:4],
        uuid[20:],
    ])


def new() -> str:
    """
    Generates a new UUID and returns
    the corresponding base64 GUID representation.
    """
    uuid = uuid4().hex
    guid = compress(uuid)
    return guid

# ----------------------------------------------------------------
# PRIVATE METHODS
# ----------------------------------------------------------------


def repr_to_int(
    s: str,
    /,
    *,
    alphabet: str = CHARS64,
) -> int:
    """
    Converts a number in a given base to an integer.
    """
    base = len(alphabet)
    digits = map(lambda a: alphabet.index(a), s)
    n = reduce(lambda x, y: base * x + y, digits, 0)
    return n


def int_to_repr(
    n: int,
    /,
    *,
    alphabet: str = CHARS64,
    padding: int | None = None,
) -> str:
    """
    Converts a positive integer to a number represented
    as a sequence of "digits" defined from an alphabet.
    """
    base = len(alphabet)

    # compute digits
    digits = []
    while n > 0:
        digits.append(n % base)
        n = n // base

    # optional padding
    if padding is not None and padding > 0:
        digits = digits[:padding]
        digits += [0] * (len(digits) - padding)

    # reverse order for left-to-right reading
    digits.reverse()

    # encode as string using symbol-set
    s = "".join(map(lambda digit: alphabet[digit], digits))

    return s
