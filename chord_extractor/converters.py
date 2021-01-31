import os
import subprocess
import logging

_log = logging.getLogger(__name__)


def midi_to_wav(midi_path: str, wav_to_dir: str):
    base = os.path.basename(midi_path)
    file_name = os.path.splitext(base)[0]
    wav_file = os.path.join(wav_to_dir, file_name)
    if not os.path.isfile(wav_file):
        _log.info('Running timidity on {} to create {}'.format(midi_path, wav_file))
        subprocess.run(['timidity', midi_path, '-Ow', '-o', wav_file])
    else:
        _log.info('Returning already existing temporary wav file {}'.format(wav_file))
    return wav_file
