"""
Python library for extracting chord sequences from sound files of multiple formats with the option of leveraging
multiprocessing to source data from many files quickly. The extraction process wraps Chordino
(http://www.isophonics.net/nnls-chroma) but is extensible to easily incorporate additional techniques.

Simple usage::

    from chord_extractor.extractors import Chordino

    chordino = Chordino(roll_on=1)

    # Optional, only if we need to extract from a file that isn't accepted by librosa
    conversion_file_path = chordino.preprocess('/some_path/some_song.mid')

    chords = chordino.extract(conversion_file_path)

Extract from many files with multiprocessing::

    from chord_extractor.extractors import Chordino
    from chord_extractor import clear_conversion_cache, LabelledChordSequence

    files_to_extract_from = [
      '/path/file1.mid',
      '/path/file2.wav',
      '/path/file3.mp3',
      '/path/file4.ogg'
    ]

    def save_to_db_cb(results: LabelledChordSequence):
        # Every time one of the files has had chords extracted, receive the chords here
        # along with the name of the original file and then run some logic here, e.g. to
        # save the latest data to DB

    chordino = Chordino(roll_on=1)

    # Optionally clear cache of file conversions (e.g. wav files that have been converted from midi)
    clear_conversion_cache()
    res = chordino.extract_many(files_to_extract_from, callback=save_to_db_cb, num_extractors=2,
                                num_preprocessors=2, max_files_in_cache=10, stop_on_error=False)
"""

from .base import ChordExtractor, clear_conversion_cache
from .outputs import ChordChange, LabelledChordSequence

__all__ = ['ChordExtractor', 'clear_conversion_cache', 'ChordChange', 'LabelledChordSequence']
