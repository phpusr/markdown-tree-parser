import unittest

from parser import Parser


class TestParser(unittest.TestCase):

    def test_parse(self):
        text = '''
Title
======

 Sub Title
 ---------

# Hello
Some text

 # Hello 2

## Hello 3
Hello from Russia
'''

        out = Parser().parse(text)

        self.assertEqual(out.title, 'Title')
        self.assertEqual(out.source, '\n')

        self.assertEqual(out.root.text, 'Title')
        self.assertEqual(out.root.source, '\n')

        self.assertEqual(out.root[0].text, 'Sub Title')
        self.assertEqual(out.root[0].source, '\n')

        self.assertEqual(out[0].text, 'Hello')
        self.assertEqual(out[0].source, 'Some text\n\n')

        self.assertEqual(out[1].text, 'Hello 2')
        self.assertEqual(out[1].source, '\n')

        self.assertEqual(out[1][0].text, 'Hello 3')
        self.assertEqual(out[1][0].source, 'Hello from Russia\n')

        self.assertEqual(out.full_source, text)


if __name__ == '__main__':
    unittest.main()
