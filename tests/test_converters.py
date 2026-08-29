from unittest import mock
from chord_extractor.converters import midi_to_wav


def test_midi_to_wav_suppress_output():
    with mock.patch('subprocess.run') as run, mock.patch('os.path.isfile', return_value=False):
        run.return_value = mock.Mock(stdout='')
        midi_to_wav('/tmp/foo.mid', '/tmp/out', suppress_output=True)
        assert run.call_args.kwargs['stderr'] is not None


def test_midi_to_wav_default_does_not_suppress_output():
    with mock.patch('subprocess.run') as run, mock.patch('os.path.isfile', return_value=False):
        run.return_value = mock.Mock(stdout='')
        midi_to_wav('/tmp/foo.mid', '/tmp/out')
        assert run.call_args.kwargs['stderr'] is None
