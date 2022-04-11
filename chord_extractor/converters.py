#!/usr/bin/env python

# Chord Extractor
# Copyright (C) 2021-22  Oliver Holloway
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os
import subprocess
import logging

_log = logging.getLogger(__name__)


def midi_to_wav(midi_path: str, wav_to_dir: str):
    """
    Convert midi at given path to wav file and save in specified output directory. This is done using
    Timidity (http://timidity.sourceforge.net/). If an invalid midi file is passed, note that no exception is raised
    and an output file containing invalid wav data.

    :param midi_path: Path to input midi file
    :param wav_to_dir: Path to the output directory
    :return: Path to the new wav file
    """
    base = os.path.basename(midi_path)
    file_name = os.path.splitext(base)[0]
    wav_file = os.path.join(wav_to_dir, file_name)
    if not os.path.isfile(wav_file):
        _log.info('Running timidity on {} to create {}'.format(midi_path, wav_file))
        subprocess.run(['timidity', midi_path, '-Ow', '-o', wav_file])
    else:
        _log.info('Returning already existing temporary wav file {}'.format(wav_file))
    return wav_file
