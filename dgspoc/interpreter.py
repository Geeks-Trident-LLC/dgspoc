"""Module containing the logic for describe-get-system to interpret
user describing problem"""


import re


class Statement:
    def __init__(self, data, parent=None):
        self.data = data
        self.prev = None
        self.next = None
        self.parent = parent
        self._children = []
        self._name = ''
        self._is_parsed = False
        self._stmt_data = ''
        self._remaining_data = ''
        self.prepare()

    def __len__(self):
        return True

    @property
    def is_parsed(self):
        return self._is_parsed

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def is_empty(self):
        return self.data.strip() != ''

    @property
    def is_statement(self):
        return self._name != ''

    @property
    def statement_data(self):
        return self._stmt_data

    @property
    def remaining_data(self):
        return self._remaining_data

    def prepare(self):
        if self.is_empty:
            self._stmt_data = ''
            self._remaining_data = ''
        else:
            lst = self.data.splitlines()
            for index, line in enumerate(lst):
                line = str(line).rstrip()
                if line.strip():
                    self._stmt_data = line
                    self._remaining_data = '\n'.join(lst[index:])


class DummyStatement(Statement):
    def __init__(self, data, parent=None):
        super().__init__(data, parent=parent)
        self.case = ''
        self.msg = ''
        self.parse()

    def parse(self):
        pattern = '(?i) *dummy(?P<case>pass|fail) *[^a-z0-9]*(?P<msg> *.+) *$'
        match = re.match(pattern, self.statement_data)
        if match:
            self._is_parsed = True
            self.case = match.group('case').lower()
            self.msg = match.group('msg')
        else:
            self._is_parsed = False


class SectionStatement(Statement):
    def __init__(self, data, parent=None):
        super().__init__(data, parent=parent)


class LoopStatement(Statement):
    def __init__(self, data, parent=None):
        super().__init__(data, parent=parent)


class PerformerStatement(Statement):
    def __init__(self, data, parent=None):
        super().__init__(data, parent=parent)


class VerificationStatement(Statement):
    def __init__(self, data, parent=None):
        super().__init__(data, parent=parent)


class SystemStatement(Statement):
    def __init__(self, data, parent=None):
        super().__init__(data, parent=parent)
