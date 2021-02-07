from chord_extractor.base import ChordExtractor, ChordChange
import librosa
import vamp
from typing import List
import os
import sys
from pkg_resources import resource_filename

if not os.getenv('VAMP_PATH') and sys.platform == 'linux' and sys.maxsize > 2**32:
    os.environ['VAMP_PATH'] = os.path.dirname(resource_filename('chord_extractor', '_lib/nnls-chroma.so'))


class Chordino(ChordExtractor):
    """
    Class for extracting chords using Chordino (http://www.isophonics.net/nnls-chroma).
    """
    def __init__(self, params: dict = None):
        super().__init__()
        if params is None:
            params = {'rollon': 1}
        self._params = params

    def extract(self, filepath: str, **kwargs) -> List[ChordChange]:
        """
        Extract chord changes from a particular file. The file is loaded into librosa, therefore takes sound files
        supported by librosa (which uses audioread and soundfile). This includes .wav, .mp3, .ogg and others.

        :param filepath: Absolute file path to the relevant file. A file like object is also acceptable.
        :param kwargs: Keyword arguments for librosa.load
         (see https://librosa.org/doc/0.7.0/generated/librosa.core.load.html)
        :return: List of chord changes for the sound file
        """
        data, rate = librosa.load(filepath, **kwargs)
        chords = vamp.collect(data, rate, 'nnls-chroma:chordino', parameters=self._params)
        return [ChordChange(timestamp=float(change['timestamp']),
                            chord=change['label']) for change in chords['list'][1:-1]]

