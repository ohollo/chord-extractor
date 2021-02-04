from .base import ChordExtractor, ChordChange
import librosa
import vamp
from typing import List
import logging, os, sys
from pkg_resources import resource_filename

if not os.getenv('VAMP_PATH') and sys.platform == 'linux' and sys.maxsize > 2**32:
    os.environ['VAMP_PATH'] = os.path.dirname(resource_filename('chord_extractor', 'lib/nnls-chroma.so'))


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

