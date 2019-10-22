from parser import Parser

text = '''
# Hello
Some text

 # Hello 2

## Hello 3
Hello from Russia
'''

out = Parser().parse(text)
assert out.title == 'Hello'
assert out.source == '\n'

assert out.root.text == 'Hello'
assert out.root.source == 'Some text\n\n'

assert out[0].text == 'Hello 2'
assert out[0].source == '\n'

assert out[0][0].text == 'Hello 3'
assert out[0][0].source == 'Hello from Russia\n'

assert out.full_source == text

