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
assert out[0].text == 'Hello 2'
assert out[0][0] == 'Hello 3'

