import os
from .base import ChordExtractor, ChordChange
import librosa
import vamp
from typing import List

# os.environ["VAMP_PATH"] = '/home/ubuntu/nnls-chroma-linux64-v1.1'


class Chordino(ChordExtractor):
    def __init__(self, params: dict = None):
        super().__init__()
        if params is None:
            params = {'rollon': 1}
        self._params = params

    def extract(self, file: str) -> List[ChordChange]:
        data, rate = librosa.load(file)
        chords = vamp.collect(data, rate, 'nnls-chroma:chordino', parameters=self._params)
        return [ChordChange(timestamp=float(change['timestamp']), chord=change['label']) for change in chords['list']]
