from .base import ChordExtractor, ChordChange
import librosa
import vamp
from typing import List
import logging, os


class Chordino(ChordExtractor):
    def __init__(self, params: dict = None):
        super().__init__()
        if params is None:
            params = {'rollon': 1}
        self._params = params

    def extract(self, file: str) -> List[ChordChange]:
        logging.info(os.environ['VAMP_PATH'])
        data, rate = librosa.load(file)
        chords = vamp.collect(data, rate, 'nnls-chroma:chordino', parameters=self._params)
        return [ChordChange(timestamp=float(change['timestamp']), chord=change['label']) for change in chords['list']]
