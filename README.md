
markdown-tree-parser
====================

Parse markdown file to python object, which contains markdown tree headings

### Usage examples

```python
def test_code_block(self):
        text = '''
Title
=====

# Code

Code 1
------
Some text
\```
# TODO
\```

Code 2
------
\```python
# TODO
print('test')
\```

# Heading
'''
        out = parse_string(text)
        self.assertEqual(out.title, 'Title')
        self.assertEqual(out[0][0].text, 'Code 1')
        self.assertEqual(out[0][0].source, 'Some text\n```\n# TODO\n```\n')
        self.assertEqual(out[0][1].text, 'Code 2')
        self.assertEqual(out[0][1].source, "```python\n# TODO\nprint('test')\n```\n")
        self.assertEqual(out[1].text, 'Heading')
```
