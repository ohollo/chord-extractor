from abc import ABC, abstractmethod
from typing import List, Callable, NamedTuple, Tuple, Optional
import multiprocessing as mp
from .converters import midi_to_wav
import logging
import os
import glob


_log = logging.getLogger(__name__)
_tmp_root = os.getenv('EXTRACTOR_TEMP_FILE_PATH', '/tmp/')
_tmp_dir = os.path.join(_tmp_root, 'extractor/')
if not os.path.exists(_tmp_dir):
    os.makedirs(_tmp_dir)


def _convert_to_intermediate_file(instance, path, extract_q, file_count_q):
    file_count_q.put(path)
    intermediate_file = getattr(instance, 'convert')(path)
    extract_q.put((intermediate_file, True) if intermediate_file else (path, False))


class ChordChange(NamedTuple):
    """Tuple to represent the time point in a sound file at which a chord changes and which chord it changes to"""
    chord: str
    timestamp: float


def clear_conversion_cache():
    files = glob.glob(os.path.join(_tmp_dir, '*'))
    for f in files:
        os.remove(f)


class ChordExtractor(ABC):
    """
    Abstract class for extracting chords from sound files. It also provides functionality for sound file conversion,
    which can be added to by overriding .convert. This is useful as implementations using .extract
    may take only certain file formats, and integrating conversion logic here enables it to be parallelized.
    """
    @abstractmethod
    def extract(self, filepath: str) -> List[ChordChange]:
        """
        Extract chord changes from a particular file

        :param filepath: Absolute file path to the relevant file
        :return: List of chord changes for the sound file
        """

    @staticmethod
    def convert(path: str) -> Optional[str]:
        """
        Convert file at the path to a wav file if it has a file format which can be converted (currently midi)

        :param path: Path to the file
        :return: Return file path to output file of conversion if conversion has happened, else None
        """
        ext = os.path.splitext(path)[1]
        if ext in ['.mid', '.midi']:
            return midi_to_wav(path, _tmp_dir)
        return None

    def extract_many(self,
                     files: List[str],
                     callback: Callable[[List[ChordChange], str], None] = None,
                     num_extraction_processes: int = 1,
                     num_conversion_processes: int = 1,
                     max_files_in_cache: int = 50) -> List[Tuple[List[ChordChange], str]]:
        """
        Extract chords from a list of files. As opposed to looping over the .extract method, this one gives the option
        to run many extractions in parallel. Furthermore any file conversions that have to be done as a prerequisite
        to extraction can also be done in parallel with the extractions.

        Files can be a mix of different file formats. If they are deemed to be needing conversion, they will be and
        then the conversion will be passed to a queue for extraction. Otherwise the original file will be queued.
        Any conversions will be cached in a temporary folder specified using the environment variable
        EXTRACTOR_TEMP_FILE_PATH.

        :param files: List of paths to files we wish to extract chords for
        :param callback: An optional callable that is called when chords have been extracted from a particular file.
         This takes a tuple with the extraction results and original filepath of the extracted file as argument.
        :param num_extraction_processes: Max number of extraction processes to run in parallel
        :param num_conversion_processes: Max number of conversion processes to run in parallel
        :param max_files_in_cache: Limit of number of files for a single extract_many run to have in the temporary file
         cache (for file conversions) at any one time. If 0, there is no limit.
        :return: List of tuples, each with the extraction results and original filepath
        """
        m = mp.Manager()
        extract_q = m.Queue()
        file_count_q = m.Queue(maxsize=max_files_in_cache)
        conversion_pool = mp.Pool(processes=num_conversion_processes)
        extractor_pool = mp.Pool(processes=num_extraction_processes)
        conversions = [conversion_pool.apply_async(_convert_to_intermediate_file,
                                                   args=(self, file, extract_q, file_count_q))
                       for file in files]
        extractions = []
        while len(extractions) < len(files):
            path, remove_path = extract_q.get()
            extractions.append(extractor_pool.apply_async(self._consume,
                                                          args=(path, file_count_q),
                                                          kwds={'remove_path': remove_path and not not max_files_in_cache},
                                                          callback=callback))
        for c in conversions:
            c.get()
        res = [a.get() for a in extractions]
        return res

    def _consume(self, path, file_count_q, remove_path=False):
        res = self.extract(path)
        original_path = file_count_q.get()
        if remove_path:
            os.remove(path)
        return res, original_path
