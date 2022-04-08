"""Module containing the logic for describe-get-system to interpret
user describing problem"""


import re

# from dgspoc.utils import DictObject
from dgspoc.utils import Misc

from dgspoc.constant import FWTYPE

from dgspoc.exceptions import NotImplementedFrameworkError


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
        return self.data.strip() == ''

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

    @classmethod
    def get_display_statement(cls, framework='', message='', is_logger=False):
        func_name = 'self.logger.info' if is_logger else 'print'
        if framework == FWTYPE.UNITTEST:
            stmt = '{}({!r})'.format(func_name, message)
            return stmt
        elif framework == FWTYPE.PYTEST:
            stmt = '{}({!r})'.format(func_name, message)
            return stmt
        elif framework == FWTYPE.ROBOTFRAMEWORK:
            stmt = 'log   {}'.format(message)
            return stmt
        else:
            stmt = '{}({!r})'.format('print', message)
            return stmt

    @classmethod
    def get_assert_statement(cls, expected_result, result='', framework=''):

        is_eresult_number, eresult = Misc.try_to_get_number(expected_result)
        if Misc.is_boolean(eresult):
            eresult = int(eresult)

        if framework == FWTYPE.UNITTEST:
            fmt1 = 'self.assertTrue({} == {})'
            fmt2 = 'total_count = len(result)\nself.assertTrue(total_count == {})'
            if result:
                stmt = fmt1.format(result, expected_result)
                return stmt
            else:
                stmt = fmt2.format(eresult)
                return stmt
        elif framework == FWTYPE.PYTEST:
            fmt1 = 'assert {} == {}'
            fmt2 = 'total_count = len(result)\nassert total_count == {}'
            if result:
                stmt = fmt1.format(result, expected_result)
                return stmt
            else:
                stmt = fmt2.format(eresult)
                return stmt

        elif framework == FWTYPE.ROBOTFRAMEWORK:
            fmt1 = 'should be true   {} == {}'
            fmt2 = ('${total_count}=   get length ${result}\nshould be '
                    'true   ${result} == %s')
            if result:
                stmt = fmt1.format(result, expected_result)
                return stmt
            else:
                stmt = fmt2 % eresult
                return stmt
        else:
            failure = '{!r} test framework is not implement.'.format(framework)
            NotImplementedFrameworkError(failure)


class DummyStatement(Statement):
    def __init__(self, data, parent=None):
        super().__init__(data, parent=parent)
        self.case = ''
        self.message = ''
        self.parse()

    def parse(self):
        pattern = ' *dummy[_. -]*(?P<case>pass|fail) *[^a-z0-9]*(?P<message> *.+) *$'
        match = re.match(pattern, self.statement_data, re.I)
        if match:
            self._is_parsed = True
            self.case = match.group('case').lower()
            self.message = match.group('message')
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
