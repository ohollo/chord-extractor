from abc import ABC, abstractmethod
from typing import List, Callable, NamedTuple, Tuple
import multiprocessing as mp
from .converters import midi_to_wav
import logging
import os


log = logging.getLogger(__name__)

tmp_root = os.getenv('EXTRACTOR_TEMP_FILE_PATH', '/tmp/')
tmp_dir = os.path.join(tmp_root, 'extractor/')
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)


class ChordChange(NamedTuple):
    chord: str
    timestamp: float


def _convert_to_intermediate_file(instance, path, extract_q, file_count_q):
    file_count_q.put(path)
    intermediate_file = getattr(instance, 'convert')(path)
    extract_q.put((intermediate_file, True) if intermediate_file else (path, False))


class ChordExtractor(ABC):
    @abstractmethod
    def extract(self, filepath: str) -> List[ChordChange]:
        pass

    def convert(self, path: str):
        ext = os.path.splitext(path)[1]
        if ext in ['.mid', '.midi']:
            return midi_to_wav(path, tmp_dir)
        return None

    def extract_many(self,
                     files: List[str],
                     callback: Callable[[List[ChordChange]], None] = None,
                     num_extraction_processes: int = 1,
                     num_conversion_processes: int = 1,
                     max_files_in_cache: int = 50) -> List[Tuple[List[ChordChange], str]]:
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
            print(remove_path)
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
