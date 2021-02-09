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
