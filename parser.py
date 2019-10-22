import re


class Element:
    def __init__(self):
        self._source = ''
        self.children = []

    def add_child(self, el):
        self.children.append(el)

    def add_source(self, source):
        self._source += source

    def __getitem__(self, item):
        return self.children[item]

    @property
    def source(self):
        return self._source

    @property
    def full_source(self):
        return ''.join([x.full_source for x in self.children])


class Out(Element):
    root = None

    @property
    def title(self):
        if self.root is not None:
            return self.root.text

    @property
    def full_source(self):
        return f'{self._source}{self.root.full_source}{super().full_source}'


class Heading(Element):
    def __init__(self, parent, level, text, text_source):
        super().__init__()
        self.parent = parent
        self.level = level
        self.text = text
        self.text_source = text_source

    @property
    def full_source(self):
        return f'{self.text_source}\n{self._source}{super().full_source}'

    def __str__(self):
        return self.text


class Parser:
    DEBUG = False

    def parse(self, text):
        self.out = Out()
        self.current = None

        strings = text.split('\n')
        for index in range(len(strings)):
            string = strings[index]
            is_heading = False
            for level in range(6):
                is_heading = self._parse_heading(level + 1, string)
                if is_heading:
                    break
                # TODO parse heading with '---' and '==='

            if not is_heading:
                ending = '' if index == len(strings) - 1 else '\n'
                if self.current is None:
                    self.out.add_source(string + ending)
                else:
                    self.current.add_source(string + ending)

        return self.out

    def _parse_heading(self, level, string):
        if False:
            print(f' - parse heading with level: {level}, string: {string}')

        regex = '^(\s?#{%s}\s+)(.*)$' % level
        result = re.search(regex, string)

        if result is None:
            return False

        text = result[2]
        text_source = result[1] + text

        if self.current is None:
            parent = self.out
        elif level > self.current.level:
            parent = self.current
        else:
            parent = self.current.parent

        self.current = Heading(parent, level, text, text_source)

        if level == 1 and self.out.root is None:
            self.out.root = self.current
        else:
            parent.add_child(self.current)

        if self.DEBUG:
            print(f'Create: {str(self.current)}')

        return True
