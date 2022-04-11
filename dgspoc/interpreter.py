"""Module containing the logic for describe-get-system to interpret
user describing problem"""


import re

# from dgspoc.utils import DictObject
from dgspoc.utils import Misc

from dgspoc.constant import FWTYPE

from dgspoc.exceptions import NotImplementedFrameworkError


class Statement:
    def __init__(self, data, parent=None, framework=''):
        self.data = data
        self.prev = None
        self.next = None
        self.current = None
        self.parent = parent
        self.framework = str(framework).strip()
        self._children = []
        self._name = ''
        self._is_parsed = False
        self._stmt_data = ''
        self._remaining_data = ''
        self.validate_framework()
        self.prepare()

    def __len__(self):
        return 1 if self.name != '' else 0

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

    def validate_framework(self):

        if self.framework.strip() == '':
            failure = 'framework MUST be "unittest", "pytest", or "robotframework"'
            raise NotImplementedFrameworkError(failure)

        is_valid_framework = self.framework == FWTYPE.UNITTEST
        is_valid_framework |= self.framework == FWTYPE.PYTEST
        is_valid_framework |= self.framework == FWTYPE.ROBOTFRAMEWORK

        if not is_valid_framework:
            fmt = '{!r} framework is not implemented.'
            raise NotImplementedFrameworkError(fmt.format(self.framework))

    def get_display_statement(self, message=''):
        message = getattr(self, 'message', message)
        is_logger = getattr(self, 'is_logger', False)
        func_name = 'self.logger.info' if is_logger else 'print'
        if self.framework == FWTYPE.UNITTEST:
            stmt = '{}({!r})'.format(func_name, message)
            return stmt
        elif self.framework == FWTYPE.PYTEST:
            stmt = '{}({!r})'.format(func_name, message)
            return stmt
        else:   # i.e ROBOTFRAMEWORK
            stmt = 'log   {}'.format(message)
            return stmt

    def get_assert_statement(self, expected_result, assert_only=False):
        is_eresult_number, eresult = Misc.try_to_get_number(expected_result)
        if Misc.is_boolean(eresult):
            eresult = int(eresult)

        if self.framework == FWTYPE.UNITTEST:
            fmt1 = 'self.assertTrue(True == {})'
            fmt2 = 'total_count = len(result)\nself.assertTrue(total_count == {})'
        elif self.framework == FWTYPE.PYTEST:
            fmt1 = 'assert True == {}'
            fmt2 = 'total_count = len(result)\nassert total_count == {}'
        else:   # i.e ROBOTFRAMEWORK
            fmt1 = 'should be true   True == {}'
            fmt2 = ('${total_count}=   get length ${result}\nshould be '
                    'true   ${result} == %s')

        fmt = fmt1 if assert_only else fmt2
        eresult = expected_result if assert_only else eresult
        stmt = fmt.format(eresult)
        return stmt


class DummyStatement(Statement):
    def __init__(self, data, parent=None, framework=''):
        super().__init__(data, parent=parent, framework=framework)
        self.case = ''
        self.message = ''
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        fmt = 'DUMMY {} - {}'
        expected_result = True if self.case.lower() == 'pass' else False

        message = fmt.format(self.case.upper(), self.message)
        displayed_stmt = self.get_display_statement(message=message)
        assert_stmt = self.get_assert_statement(expected_result, assert_only=True)
        return '{}\n{}'.format(displayed_stmt, assert_stmt)

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
    def __init__(self, data, parent=None, framework=''):
        super().__init__(data, parent=parent, framework=framework)


class LoopStatement(Statement):
    def __init__(self, data, parent=None, framework=''):
        super().__init__(data, parent=parent, framework=framework)


class PerformerStatement(Statement):
    def __init__(self, data, parent=None, framework=''):
        super().__init__(data, parent=parent, framework=framework)


class VerificationStatement(Statement):
    def __init__(self, data, parent=None, framework=''):
        super().__init__(data, parent=parent, framework=framework)


class SystemStatement(Statement):
    def __init__(self, data, parent=None, framework=''):
        super().__init__(data, parent=parent, framework=framework)
