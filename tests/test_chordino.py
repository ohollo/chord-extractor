from chord_extractor.chordino import Chordino
import os
import logging
from os.path import abspath, join, realpath, isfile
from timeit import default_timer
import json


os.environ["VAMP_PATH"] = '/home/ubuntu/nnls-chroma-linux64-v1.1'

sample_file_dir = abspath(join(realpath(__file__), '../data'))
out_dir = abspath(join(realpath(__file__), '../out'))


def _get_files_in_dir(dir):
    return [abspath(join(dir, f)) for f in os.listdir(dir) if (isfile(join(dir, f)))]

def _remove_files(dir):
    for f in _get_files_in_dir(dir):
        os.remove(f)

sample_files = _get_files_in_dir(sample_file_dir)


def output_file(chord_list):
    base = os.path.basename(chord_list[1])
    with open(os.path.join(out_dir, os.path.splitext(base)[0]), 'w') as f:
        json.dump(chord_list, f)
    return chord_list


def test_extract_many():
    _remove_files(out_dir)
    start = default_timer()
    c = Chordino()
    clear_conversion_cache()
    c.extract_many(sample_files,
                   num_extraction_processes=2,
                   num_conversion_processes=2,
                   max_files_in_cache=3,
                   callback=output_file)
    end = default_timer()
    print(end - start)


def test_extract():
    start = default_timer()
    c = Chordino()
    for s in sample_files:
        conversion = c.convert(s)
        if conversion:
            c.extract(conversion)
            os.remove(conversion)
        else:
            c.extract(s)
    end = default_timer()
    print(end - start)

