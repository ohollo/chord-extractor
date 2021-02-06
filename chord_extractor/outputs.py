from typing import NamedTuple, List


class ChordChange(NamedTuple):
    """Tuple to represent the time point in a sound file at which a chord changes and which chord it changes to."""
    chord: str
    timestamp: float


class LabelledChordSequence(NamedTuple):
    """Output of chord extractions with id suitable for when running using asynchronous processes"""
    id: str
    sequence: List[ChordChange]
