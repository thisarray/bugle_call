"""Print the array of tones from a string of notes and a tempo."""

import json
import unittest

# High C (C6) is seldomly used
# High B flat (B6b) is only found in a few marches
BUGLE_NOTES = ('C4', 'G4', 'C5', 'E5', 'G5', 'C6')
"""Tuple of string notes that can be played by a bugle."""

def bpm_to_duration(bpm):
    """Return a duration in seconds from bpm beats per minute."""
    if not isinstance(bpm, int):
        raise TypeError('bpm must be a positive int.')
    if bpm <= 0:
        raise ValueError('bpm must be a positive int.')
    return (60.0 / bpm)

class _UnitTest(unittest.TestCase):
    def test_BUGLE_NOTES(self):
        """Test the notes that can be played by a bugle."""
        for value in BUGLE_NOTES:
            self.assertEqual(value.upper(), value)
            self.assertIn(value.upper(), BUGLE_NOTES)
        for value in ['A4', 'A5', 'B4', 'B5', 'D4', 'D5', 'F4', 'F5']:
            self.assertNotIn(value, BUGLE_NOTES)

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
    import json
    import os.path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-c', '--check', default='',
        help='check the bugle calls in the JSON file at path')
    parser.add_argument(
        '-t', '--tempo', type=int, default=60,
        help='integer number of quarter notes per minute in the bugle call')
    parser.add_argument(
        'notes', nargs='?', default='',
        help='string of notes in the bugle call')
    args = parser.parse_args()

    if os.path.isfile(args.check):
        with open(args.check, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        print('Found {} bugle calls'.format(len(json_data)))
        for name, value in json_data.items():
            for note in value:
                length = len(note)
                if (length < 2) or (3 < length):
                    print('Invalid note array in {}!'.format(name))
                    continue
                if note[0] not in BUGLE_NOTES:
                    print('Invalid note in {}: {}'.format(name, note[0]))
                if (note[1] < 0) or (30 < note[1]):
                    print('Invalid duration in {}: {}'.format(name, note[1]))
                if (length == 3) and ((note[2] < 0) or (10 < note[2])):
                    print('Invalid rest in {}: {}'.format(name, note[2]))
    elif len(args.notes) > 0:
        if (len(args.notes) % 2) != 0:
            parser.error('String of notes must have an even length.')

        duration = bpm_to_duration(args.tempo)
        note_array = []
        i = 0
        while i < len(args.notes):
            note = args.notes[i:i+2].upper()
            if note not in BUGLE_NOTES:
                parser.error('Invalid note: {}'.format(note))
            note_array.append([note, duration])
            i += 2

        # Print the durations
        durations = []
        for label, divisor in [
            ('Whole', 0.25),
            ('Half', 0.5),
            ('Quarter', 1.0),
            ('Eighth', 2.0),
            ('Sixteenth', 4.0),
            ('Thirty-second', 8.0)]:
            padded_label = label.rjust(13)
            length = duration / divisor
            durations.append('{}\t{}'.format(padded_label + ' ', length))
            durations.append('{}\t{}'.format(padded_label + '.', 1.5 * length))
            durations.append('{}\t{}'.format(padded_label + '3', length / 3))
        for d in durations:
            print(d)
        print()

        # Print the array of tones
        print('  "name": [')
        for note in note_array:
            print('    ' + json.dumps(
                note, separators=(', ', ': '), sort_keys=True) + ',')
        print('  ]')
    else:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(_UnitTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
