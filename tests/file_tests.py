import unittest

from markdown_tree_parser.parser import parse_string


class TestParser(unittest.TestCase):

    def test_parse_todo(self):
        with open('/home/phpusr/notes/knowledge-base/linux.md') as f:
            text = f.read()

        out = parse_string(text)

        with open('out.md', 'w') as f:
            f.write(out.full_source)

        self.assertEqual(out.full_source, text)


if __name__ == '__main__':
    unittest.main()
