# chord-extractor
Python library for extracting chord sequences from sound files of multiple formats with the option of
leveraging multiprocessing to source data from many files quickly. The extraction process
wraps [Chordino](http://www.isophonics.net/nnls-chroma) but is extensible to easily incorporate 
additional techniques.

## Why?
- Primarily intended for those analysing musical pieces and their harmonic progressions. 
- [Chordino](http://www.isophonics.net/nnls-chroma) is a C++ [Vamp Plugin](https://vamp-plugins.org/) for extracting chords but even with the helpful 
  [vamp](https://pypi.org/project/vamp/) Python wrapper, it is not trivial to set everything up. This project
  aims to help clarify the prerequisites and get the user up and running with extracting chords with as little fuss as possible.
- Chord extraction of many files is time-consuming. This library gives the option of parallelization (on a particular
  machine) to cut the overall processing time considerably.   
- There are certain music files that are readily available but need converting prior to using the plugin (e.g. MIDI). 
  This preprocessing is also included and can also be extended to convert other formats or other tasks that can take  
  advantage of multiprocessing.
  
## Installation
The package is hosted on PyPI, but prior to installing that there are a few prerequisite steps. The following
instructions assume the use of Linux, and this is the recommended type of OS to use. That said, equivalent steps may be
used, e.g. if you are using another OS.
- `sudo apt-get install libsndfile1` - To read sound files.
- (OPTIONAL) `sudo apt-get install timidity` - If wanting to extract chords from MIDIs (timidity converts midi to wav files).
- (OPTIONAL) `sudo apt-get install ffmpeg` - If wanting to extract from mp3s
- `pip install numpy` - numpy needs to be installed in your Python environment *prior* to installing chord-extractor. 
This is necessary as one of the package dependencies (vamp) requires it in its setup.py.
  
## Usage

Extract chords from a single file:

```python
from chord_extractor.extractors import Chordino

chordino = Chordino(params={'rollon': 1})

# Optional, only if we need to extract from a file that isn't accepted by librosa
conversion_file_path = chordino.preprocess('/some_path/some_song.mid')

chords = chordino.extract(conversion_file_path)
```

To perform extraction of many files, even with various file types, we can pass a list of files in a single 
function. Here we can have 2 conversions running in parallel (preprocessing), and 2 extractions in parallel.

```python
from chord_extractor.extractors import Chordino
from chord_extractor import clear_conversion_cache, LabelledChordSequence

files_to_extract_from = [
  '/path/file1.mid',
  '/path/file2.wav',
  '/path/file3.mp3',
  '/path/file4.ogg'
]

def save_to_db_cb(results: LabelledChordSequence):
    # Every time one of the files has had chords extracted, receive the chords here along with the name 
    # of the original file and then run some logic here, e.g. to save the latest data to DB

chordino = Chordino(params={'rollon': 1})

# Optionally clear cache of converted files (e.g. midi files that have been converted to wav for extraction)
clear_conversion_cache()
res = chordino.extract_many(files_to_extract_from, callback=save_to_db_cb, num_extractors=2,
                            num_preprocessors=2, max_files_in_cache=10, stop_on_error=False)
```

If you want to implement your own extraction logic and/or add functionality to convert from another file format, whilst
still taking advantage of the inbuilt multiprocessing logic, this can be done by extending the base class ChordExtractor
```python
from chord_extractor import ChordExtractor, ChordChange
from typing import Optional, List
import os

class MyExtractor(ChordExtractor):
    def __init__(self, some_new_setting):
      self.some_new_setting = ####
    
    def preprocess(self, path: str) -> Optional[str]:
        conversion_path = super().preprocess(path)
        ext = os.path.splitext(path)[1]
        if ext in ['.newfmt']:
          conversion_path = # preprocess file at path, convert to .newfmt and have path to new temporary file
        return conversion_path
    
    def extract(self, filepath: str) -> List[ChordChange]:
        # Custom extraction logic using self.some_new_setting perhaps
```

See technical documentation for more details.

