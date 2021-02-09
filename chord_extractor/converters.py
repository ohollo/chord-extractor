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
