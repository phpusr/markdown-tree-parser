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
        return f'{self.text_source}\n{self._source}{super().full_source}'

    def __str__(self):
        return self.text


class Parser:
    DEBUG = not False

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
                ending = '' if index == len(strings) - 1 else '\n'
                if self.current is None:
                    self.out.add_source(string + ending)
                else:
                    self.current.add_source(string + ending)

        return self.out

    def _parse_heading_var_one(self, level, string, next_string):
        if next_string is None:
            return False

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
        if False:
            print(f' - parse heading with level: {level}, string: {string}')

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
            level_diff = self.current.level - level + 1
            tmp_current = self.current
            for index in range(level_diff):
                parent = tmp_current.parent
                tmp_current = parent

        self.current = Heading(parent, level, text, text_source)

        if level == 1 and self.out.root is None:
            self.out.root = self.current
        else:
            parent.add_child(self.current)

        if self.DEBUG:
            spaces = '  '.join(['' for _ in range(parent.level + 1)]) if parent != self.out else ''
            print(f'{spaces}<{str(parent)}>')
            spaces = '  '.join(['' for _ in range(self.current.level + 1)])
            print(f'{spaces}<{str(self.current)}> (+)')

        return True
