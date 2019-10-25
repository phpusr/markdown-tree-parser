import re


def parse_string(string, debug_level=0):
    return Parser(debug_level).parse(string)


def parse_file(file_path, debug_level=0):
    with open(file_path) as f:
        return parse_string(f.read(), debug_level)


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

    def __len__(self):
        return len(self.children)

    @property
    def source(self):
        return self._source

    @property
    def full_source(self):
        if len(self.children) == 0:
            return ''

        return '\n' + '\n'.join([x.full_source for x in self.children])


class Out(Element):
    main = None
    level = 0

    @property
    def title(self):
        if self.main is not None:
            return self.main.text

    @property
    def full_source(self):
        result = ''
        if self._source is not None:
            result += f'{self._source}\n'
        result += self.main.full_source
        result += super().full_source
        return result

    def __str__(self):
        return 'Out'


class Heading(Element):
    def __init__(self, root, parent, level, text, text_source):
        super().__init__()
        self.root = root
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
    def __init__(self, debug_level=0):
        self.DEBUG = debug_level

    def parse(self, text):
        self.out = Out()
        self.current = None
        jump_to_next = False
        code_block = False

        strings = text.split('\n')
        for index in range(len(strings)):
            if jump_to_next:
                jump_to_next = False
                continue

            string = strings[index]
            is_heading = False

            """ Search code block """
            if re.search(r'^\s*```.*$', string) is not None:
                code_block = not code_block

            """ Search and parse headings """
            if not code_block:
                next_string = strings[index + 1] if index + 1 < len(strings) else None

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
        if next_string is None or re.search(r'^\s*$', string) is not None:
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

        self.current = Heading(self.out, parent, level, text, text_source)

        if level == 1 and self.out.main is None:
            self.out.main = self.current
        else:
            parent.add_child(self.current)

        if self.DEBUG >= 1:
            spaces = '  '.join(['' for _ in range(parent.level + 1)]) if parent != self.out else ''
            print(f'{spaces}<{str(parent)}>')
            spaces = '  '.join(['' for _ in range(self.current.level + 1)])
            print(f'{spaces}(+) <{str(self.current)}>')

        return True
