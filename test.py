from parser import Parser

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

assert out.title == 'Title'
assert out.source == '\n'

assert out.root.text == 'Title'
assert out.root.source == '\n'

assert out.root[0].text == 'Sub Title'
assert out.root[0].source == '\n'

assert out[0].text == 'Hello'
assert out[0].source == 'Some text\n\n'

assert out[1].text == 'Hello 2'
assert out[1].source == '\n'

assert out[1][0].text == 'Hello 3'
assert out[1][0].source == 'Hello from Russia\n'

assert out.full_source == text

