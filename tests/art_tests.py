import unittest

import os

from markdown_tree_parser.parser import parse_string

tests_dir = 'tests'
current_dir = os.getcwd()
if os.path.basename(current_dir) != tests_dir:
    current_dir = os.path.join(current_dir, tests_dir)

print(f'current_dir: {current_dir}\n')


class TestParser(unittest.TestCase):

    def setUp(self):
        print('\n')

    def tearDown(self):
        print('')

    def test_parse(self):
        with open(os.path.join(current_dir, 'example_1.md')) as f:
            text = f.read()

        out = parse_string(text)

        with open(os.path.join(current_dir, 'out.md'), 'w') as f:
            f.write(out.full_source)

        self.assertEqual(out.title, 'Title')
        self.assertEqual(out.source, None)

        self.assertEqual(out.main.text, 'Title')
        self.assertEqual(out.main.source, '')

        self.assertEqual(out.main[0].text, 'Sub Title')
        self.assertEqual(out.main[0].source, '')

        self.assertEqual(out[0].text, 'Hello')
        self.assertEqual(out[0].source, 'Some text\n')

        self.assertEqual(out[1].text, 'Hello 2')
        self.assertEqual(out[1].source, '')

        self.assertEqual(out[1][0].text, 'Hello 3')
        self.assertEqual(out[1][0].source, 'Hello from Russia\n')

        part1 = out[2]
        self.assertEqual(part1.text, 'Part 1')
        self.assertEqual(part1.source, '\nThis is the main part\n')
        chapter1 = part1[0]
        self.assertEqual(chapter1.text, 'Chapter 1')
        self.assertEqual(chapter1.source, '\nLong ago, somewhere in a distant faraway galaxy.\n\nSome text...\n')
        self.assertEqual(chapter1[0].text, 'Sub Chapter 1.1')
        self.assertEqual(chapter1[0].source, '\nDance With th Dead - Sunset\n')
        chapter2 = part1[1]
        self.assertEqual(chapter2.text, 'Chapter 2')
        self.assertEqual(chapter2.source, '\nThis is the middle chapter\n')
        self.assertEqual(chapter2[0].text, 'Sub Chapter 2.1')
        self.assertEqual(chapter2[0].source, '\nDocument your code\n')
        self.assertEqual(chapter2[1].text, 'Sub Chapter 2.2')
        self.assertEqual(chapter2[1].source, '\nComponents File Manager\n')

        self.assertEqual(out.full_source, text)

    def test_heading_diff(self):
        text = '''

## Heading 3

# Heading 2
'''
        out = parse_string(text)
        self.assertEqual(out[0].text, 'Heading 3')
        self.assertEqual(out.main.text, 'Heading 2')

    def test_code_block(self):
        text = '''
Title
=====

# Code

Code 1
------
Some text
```
# TODO
```

Code 2
------
```python
# TODO
print('test')
```

# Heading
'''
        out = parse_string(text)
        self.assertEqual(out.title, 'Title')
        self.assertEqual(out[0][0].text, 'Code 1')
        self.assertEqual(out[0][0].source, 'Some text\n```\n# TODO\n```\n')
        self.assertEqual(out[0][1].text, 'Code 2')
        self.assertEqual(out[0][1].source, "```python\n# TODO\nprint('test')\n```\n")
        self.assertEqual(out[1].text, 'Heading')

    def test_split_line(self):
        text = '''
# Hello

-------

======

'''
        out = parse_string(text)
        self.assertEqual(out.title, 'Hello')
        self.assertEqual(len(out.main), 0)
        self.assertEqual(len(out), 0)

    def test_root_in_heading(self):
        text = '''
Title
=====

# Hello

## Hello 2

### Hello 3
'''
        out = parse_string(text)
        self.assertIs(out[0].root, out)
        self.assertIs(out[0][0].root, out)
        self.assertIs(out[0][0][0].root, out)


if __name__ == '__main__':
    unittest.main()
