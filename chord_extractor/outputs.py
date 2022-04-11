#!/usr/bin/env python

# Chord Extractor
# Copyright (C) 2021-22  Oliver Holloway
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from typing import NamedTuple, List, Optional


class ChordChange(NamedTuple):
    """
    Tuple to represent the time point in a sound file at which a chord changes and which chord it changes to.

    The string notation used in the chord string is standard notation (and that used by Chordino). Examples include
    Emaj7, Dm, Cb7, where maj = major, m = minor, b = flat etc. Note that if 'N' is given, this denotes no chord, e.g.
    if a part of the sound file is non-musical.
    """
    chord: str
    timestamp: float


class LabelledChordSequence(NamedTuple):
    """
    Output of chord extractions with identifier, suitable for when running using asynchronous processes. The
    sequence may be None if no result was returned for that particular id.
    """
    id: str
    sequence: Optional[List[ChordChange]]
