import re


class Element:
    _source = ''
    children = []

    def add_child(self, el):
        self.children.append(el)

    def add_source(self, source):
        self._source += source + '\n'

    def __getitem__(self, item):
        return self.children[item]


class Out(Element):
    title = None


class Heading(Element):
    def __init__(self, level, text):
        self.level = level
        self.text = text

    def __str__(self):
        return self.text


class Parser:
    def parse(self, text):
        self.out = Out()
        self.current = self.out

        for string in text.split('\n'):
            is_heading = False
            for level in range(6):
                is_heading = self.parse_heading(level + 1, string)
                if is_heading:
                    break

            if not is_heading:
                self.current.add_source(string)

        return self.out

    def parse_heading(self, level, string):
        if False:
            print(f' - parse heading with level: {level}, string: {string}')

        regex = '^\s?#{%s}\s+(.*)$' % level
        result = re.search(regex, string)
        if result is None:
            return False

        text = result[1]

        if level == 1 and self.out.title is None:
            self.out.title = text
            return True

        # TODO
        self.parent = self.current
        self.current = Heading(level, text)
        self.parent.add_child(self.current)

        print(f'Create: {str(self.current)}')
        return True
