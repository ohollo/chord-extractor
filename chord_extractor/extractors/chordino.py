from chord_extractor.base import ChordExtractor, ChordChange
import librosa
import vamp
from typing import List
from enum import Enum
import os
import sys
from pkg_resources import resource_filename
import logging

_log = logging.getLogger(__name__)

if not os.getenv('VAMP_PATH') and sys.platform == 'linux' and sys.maxsize > 2**32:
    os.environ['VAMP_PATH'] = os.path.dirname(resource_filename('chord_extractor', '_lib/nnls-chroma.so'))


class TuningMode(Enum):
    """Options for Tuning Mode parameter (see Chordino doc)"""
    GLOBAL = 0
    LOCAL = 1


class ChromaNormalization(Enum):
    """Options for Chroma Normalization parameter (see Chordino doc)"""
    NONE = 0
    MAX = 1
    L1 = 2
    L2 = 3


class Chordino(ChordExtractor):
    """
    Class for extracting chords using Chordino (http://www.isophonics.net/nnls-chroma). All parameters are those
    passed to Chordino. You can see further details of what they mean in the
    Chordino -> Parameters section in the above link. The defaults here are the suggested parameter settings for
    when extracting from a generic pop song. See the link for more recommended settings.

    :param use_nnls: Use approximate transcription (NNLS)
    :param roll_on: Spectral roll-on (range: 0 - 5)
    :param tuning_mode: Tuning mode
    :param spectral_whitening: Spectral whitening (range: 0 - 1)
    :param spectral_shape: Spectral shape (range: 0.5 - 0.9)
    :param boost_n_likelihood: Boost likelihood of the N (no chord) label
    :param kwargs: Any other parameters that may become available to the chordino vamp plugin. Param keys are the
     vamp identifier.
    """
    def __init__(self,
                 use_nnls: bool = True,
                 roll_on: float = 1,
                 tuning_mode: TuningMode = TuningMode.GLOBAL,
                 spectral_whitening: float = 1,
                 spectral_shape=0.7,
                 boost_n_likelihood: float = 0.1,
                 **kwargs):
        super().__init__()
        self._params = {
            'useNNLS': int(use_nnls),
            'rollon': roll_on,
            'tuningmode': tuning_mode.value,
            'whitening': spectral_whitening,
            's': spectral_shape,
            'boostn': boost_n_likelihood
        }
        self._params.update(kwargs)

    def extract(self, file: str, **kwargs) -> List[ChordChange]:
        """
        Extract chord changes from a particular file. The file is loaded into librosa, therefore takes sound files
        supported by librosa (which uses audioread and soundfile). This includes .wav, .mp3, .ogg and others.

        :param file: Absolute file path to the relevant file. A file like object is also acceptable.
        :param kwargs: Keyword arguments for librosa.load
         (see https://librosa.org/doc/0.7.0/generated/librosa.core.load.html)
        :return: List of chord changes for the sound file
        """
        data, rate = librosa.load(file, **kwargs)
        _log.info('Submitting {} to Chordino for chord extraction.')
        chords = vamp.collect(data, rate, 'nnls-chroma:chordino', parameters=self._params)
        return [ChordChange(timestamp=float(change['timestamp']),
                            chord=change['label']) for change in chords['list']]

