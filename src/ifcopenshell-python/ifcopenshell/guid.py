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

from base64 import b64decode
from base64 import b64encode
from functools import reduce
import re
from uuid import uuid4

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

ALT_CHARS = b"_$"

# ----------------------------------------------------------------
# PUBLIC METHODS
# ----------------------------------------------------------------


def compress(
    uuid: str,
    /,
    *,
    alt_chars: bytes = ALT_CHARS,
    remove_padding: bool = True,
) -> str:
    """
    Converts a hex-encoded encoded GUID
    to a base64-encoded UUID.
    """

    # remove possible separators
    uuid = uuid.lower()
    uuid = re.sub(pattern=r"\W", repl="", string=uuid)

    # left-pad uuid with 0s
    n = len(uuid)
    r = n % 2
    n += 2 - r if r > 0 else 0
    uuid = f"{uuid:0>{n}}"

    # convert to standard base 64
    uuid_bytes = bytes.fromhex(uuid)
    guid = b64encode(uuid_bytes, altchars=alt_chars).decode()

    # strip right-padding
    if remove_padding:
        guid = guid.rstrip("=")

    return guid


def expand(
    guid: str,
    /,
    *,
    alt_chars: bytes = ALT_CHARS,
) -> str:
    """
    Converts a base64-encoded GUID
    to a hex-encoded UUID.
    """

    # right-pad guid with "="
    n = len(guid)
    r = n % 4
    n += 4 - r if r > 0 else 0
    guid = f"{guid:=<{n}}"

    # convert to hex
    uuid = b64decode(guid, altchars=alt_chars).hex()

    return uuid


def split(uuid: str, /) -> str:
    """
    Formats a 32-character hex-encoded UUID as
    ```
    xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    ```
    """
    return "-".join(
        [
            uuid[:8],
            uuid[8:][:4],
            uuid[12:][:4],
            uuid[16:][:4],
            uuid[20:],
        ]
    )


def new() -> str:
    """
    Generates a new UUID and returns
    the corresponding base64 GUID representation.
    """
    uuid = uuid4().hex
    guid = compress(uuid)
    return guid
