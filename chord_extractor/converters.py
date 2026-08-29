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
from typing import Optional

_log = logging.getLogger(__name__)
_ERROR_SIGNAL_TEXT = "Not a MIDI file"


def midi_to_wav(midi_path: str, wav_to_dir: str, suppress_output: bool = False) -> Optional[str]:
    """
    Convert midi at given path to wav file and save in specified output directory. This is done using
    Timidity (http://timidity.sourceforge.net/). Note that no exception is raised when an invalid midi_path is given
    (None is returned).

    :param midi_path: Path to input midi file
    :param wav_to_dir: Path to the output directory
    :param suppress_output: If True, suppress the console output Timidity produces while converting (this can be
     quite verbose, printing out internal details of the midi file such as track/lyric/text events). Defaults to
     False, which preserves Timidity's normal console output.
    :return: Path to the new wav file. None if an invalid midi file is passed.
    """
    base = os.path.basename(midi_path)
    file_name = os.path.splitext(base)[0]
    wav_file = os.path.join(wav_to_dir, file_name)
    if not os.path.isfile(wav_file):
        _log.info('Running timidity on {} to create {}'.format(midi_path, wav_file))
        stderr = subprocess.DEVNULL if suppress_output else None
        result = subprocess.run(['timidity', midi_path, '-Ow', '-o', wav_file], stdout=subprocess.PIPE,
                                stderr=stderr, text=True, errors="replace")
        if _ERROR_SIGNAL_TEXT in result.stdout:
            _log.error('Invalid midi file at {}'.format(midi_path))
            return None
    else:
        _log.info('Returning already existing temporary wav file {}'.format(wav_file))
    return wav_file
