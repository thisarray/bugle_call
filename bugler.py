"""Print the array of tones from a string of notes and a tempo."""

import json
import unittest

def bpm_to_duration(bpm):
    """Return a duration in seconds from bpm beats per minute."""
    if not isinstance(bpm, int):
        raise TypeError('bpm must be a positive int.')
    if bpm <= 0:
        raise ValueError('bpm must be a positive int.')
    return (60.0 / bpm)

class _UnitTest(unittest.TestCase):
    def test_bpm_to_duration(self):
        """Test converting beats per minute to duration."""
        for value in [None, 42.0, '', []]:
            self.assertRaises(TypeError, bpm_to_duration, value)
        for value in [-1, 0]:
            self.assertRaises(ValueError, bpm_to_duration, value)

        self.assertAlmostEqual(bpm_to_duration(120), 0.5)
        self.assertAlmostEqual(bpm_to_duration(60), 1.0)
        self.assertAlmostEqual(bpm_to_duration(30), 2.0)
        self.assertAlmostEqual(bpm_to_duration(15), 4.0)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-t', '--tempo', type=int, default=60,
                        help='integer tempo of the bugle call')
    parser.add_argument('notes', nargs='?', default='',
                        help='string of notes in the bugle call')
    args = parser.parse_args()

    if len(args.notes) <= 0:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(_UnitTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
    else:
        if (len(args.notes) % 2) != 0:
            parser.error('String of notes must have an even length.')

        duration = bpm_to_duration(args.tempo)
        note_array = []
        i = 0
        while i < len(args.notes):
            note = args.notes[i:i+2]
            note_array.append([note.upper(), duration])
            i += 2

        # Print the durations
        durations = []
        for divisor in [1, 2, 4, 8, 16, 32]:
            length = duration / divisor
            durations.append((str(divisor), length))
            durations.append((str(divisor) + '.5', 1.5 * length))
        for divisor, length in durations:
            print('{}\t{}'.format(divisor, length))
        print()

        # Print the array of tones
        print('  "name": [')
        for note in note_array:
            print('    ' + json.dumps(
                note, separators=(', ', ': '), sort_keys=True) + ',')
        print('  ]')
