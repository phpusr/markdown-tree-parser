import re


def parse_string(string):
    return Parser().parse(string)


def parse_file(file_path):
    with open(file_path) as f:
        return parse_string(f.read())


class Element:
    def __init__(self):
        self._source = None
        self.children = []

    def add_child(self, el):
        self.children.append(el)

    def add_source(self, source):
        if self._source is None:
            self._source = source
        else:
            self._source += '\n' + source

    def __getitem__(self, item):
        return self.children[item]

    @property
    def source(self):
        return self._source

    @property
    def full_source(self):
        if len(self.children) == 0:
            return ''

        return '\n' + '\n'.join([x.full_source for x in self.children])


class Out(Element):
    root = None
    level = 0

    @property
    def title(self):
        if self.root is not None:
            return self.root.text

    @property
    def full_source(self):
        result = ''
        if self._source is not None:
            result += f'{self._source}\n'
        result += self.root.full_source
        result += super().full_source
        return result

    def __str__(self):
        return 'Out'


class Heading(Element):
    def __init__(self, parent, level, text, text_source):
        super().__init__()
        self.parent = parent
        self.level = level
        self.text = text
        self.text_source = text_source

    @property
    def full_source(self):
        result = f'{self.text_source}'
        if self._source is not None:
            result += f'\n{self._source}'
        result += super().full_source
        return result

    def __str__(self):
        return self.text


class Parser:
    DEBUG = 1

    def parse(self, text):
        self.out = Out()
        self.current = None
        jump_to_next = False

        strings = text.split('\n')
        for index in range(len(strings)):
            if jump_to_next:
                jump_to_next = False
                continue

            string = strings[index]
            next_string = strings[index + 1] if index + 1 < len(strings) else None
            is_heading = False

            for level in range(1, 3):
                is_heading = self._parse_heading_var_one(level, string, next_string)
                if is_heading:
                    break

            if is_heading:
                jump_to_next = True
                continue

            for level in range(1, 7):
                is_heading = self._parse_heading_var_two(level, string)
                if is_heading:
                    break

            if not is_heading:
                if self.current is None:
                    self.out.add_source(string)
                else:
                    self.current.add_source(string)

        return self.out

    def _parse_heading_var_one(self, level, string, next_string):
        if next_string is None:
            return False

        if self.DEBUG >= 2:
            print(f'- parse_heading_var_one with level: {level}, next_string: "{next_string}"')

        if level == 1:
            tmpl = '='
        elif level == 2:
            tmpl = '-'
        else:
            raise Exception(f'Not support level: {level}')

        regex = '^\s?%s{3,}\s*$' % tmpl
        result = re.search(regex, next_string)

        if result is None:
            return False

        return self._parse_heading_action(
            level=level,
            text=string.strip(),
            text_source=f'{string}\n{next_string}'
        )

    def _parse_heading_var_two(self, level, string):
        if self.DEBUG >= 2:
            print(f'- parse_heading_var_two with level: {level}, string: "{string}"')

        regex = '^(\s?#{%s}\s+)(.*)$' % level
        result = re.search(regex, string)

        if result is None:
            return False

        return self._parse_heading_action(
            level=level,
            text=result[2],
            text_source=result[1] + result[2]
        )

    def _parse_heading_action(self, level, text, text_source):
        if self.current is None:
            parent = self.out
        elif level > self.current.level:
            parent = self.current
        else:
            parent = self.current.parent
            while parent.level >= level:
                parent = parent.parent

        self.current = Heading(parent, level, text, text_source)

        if level == 1 and self.out.root is None:
            self.out.root = self.current
        else:
            parent.add_child(self.current)

        if self.DEBUG >= 1:
            spaces = '  '.join(['' for _ in range(parent.level + 1)]) if parent != self.out else ''
            print(f'{spaces}<{str(parent)}>')
            spaces = '  '.join(['' for _ in range(self.current.level + 1)])
            print(f'{spaces}<{str(self.current)}> (+)')

        return True
