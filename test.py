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

# Part 1

This is the main part

## Chapter 1

Long ago, somewhere in a distant faraway galaxy.

Some text...

### Sub Chapter 1.1

Dance With th Dead - Sunset

### Sub Chapter 1.2

Volume 40 %

### Sub Chapter 1.3

This is the preproduction for a cry for the moon

## Chapter 2

This is the middle chapter

### Sub Chapter 2.1

Document your code

### Sub Chapter 2.2

Components File Manager

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
        self.assertEqual(out[1][0].source, 'Hello from Russia\n\n')

        part1 = out[2]
        self.assertEqual(part1.text, 'Part 1')
        self.assertEqual(part1.source, '\nThis is the main part\n\n')
        chapter1 = part1[0]
        self.assertEqual(chapter1.text, 'Chapter 1')
        self.assertEqual(chapter1.source, '\nLong ago, somewhere in a distant faraway galaxy.\n\nSome text...\n\n')
        self.assertEqual(chapter1[0].text, 'Sub Chapter 1.1')
        self.assertEqual(chapter1[0].source, '\nDance With th Dead - Sunset\n\n')
        chapter2 = part1[1]
        self.assertEqual(chapter2.text, 'Chapter 2')
        self.assertEqual(chapter2.source, '\nThis is the middle chapter\n\n')
        self.assertEqual(chapter2[0].text, 'Sub Chapter 2.1')
        self.assertEqual(chapter2[0].source, '\nDocument your code\n\n')
        self.assertEqual(chapter2[1].text, 'Sub Chapter 2.2')
        self.assertEqual(chapter2[1].source, '\nComponents File Manager\n\n')

        self.assertEqual(out.full_source, text)


if __name__ == '__main__':
    unittest.main()
