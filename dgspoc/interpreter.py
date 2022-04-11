"""Module containing the logic for describe-get-system to interpret
user describing problem"""


import re

from textwrap import indent

from dgspoc.utils import DictObject
from dgspoc.utils import Misc

from dgspoc.constant import FWTYPE

from dgspoc.exceptions import NotImplementedFrameworkError


class ScriptInfo(DictObject):
    def __init__(self, *args, testcase='', **kwargs):
        super().__init__(*args, **kwargs)
        self.testcase = testcase

    def get_class_name(self):
        node = self.get(self.testcase)
        cls_name = node.get('class_name', 'TestClass') if node else 'TestClass'
        return cls_name

    def get_method_name(self, value):
        node = self.get(self.testcase)
        if node:
            for method_name, val in node.items():
                if val == value:
                    return method_name
            else:
                return 'test_step'


SCRIPTINFO = ScriptInfo()


class Statement:
    def __init__(self, data, parent=None, framework='', indentation=4):
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

        self._prev_spacers = ''
        self._spacers = ''
        self._level = 0
        self.indentation = indentation

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

    @property
    def level(self):
        return self._level

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
            spacer_pat = r'(?P<spacers> *)[^ ].*'
            for index, line in enumerate(lst):
                line = str(line).rstrip()
                if line.strip():
                    match = re.match(spacer_pat, line)
                    if match:
                        self._spacers = match.group('spacers')
                        length = len(self._spacers)
                        if length == 0:
                            self._level = 0
                        else:
                            if self.parent:
                                chk_lst = ['setup', 'cleanup', 'teardown', 'section']
                                if self.parent.name in chk_lst:
                                    self._level = 1
                                else:
                                    self._level += 1
                            else:
                                if self._prev_spacers > self._spacers:
                                    self._level += 1

                    self._prev_spacers = self._spacers
                    self._stmt_data = line
                    self._remaining_data = '\n'.join(lst[index:])
                    return

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
        elif self.framework == FWTYPE.PYTEST:
            stmt = '{}({!r})'.format(func_name, message)
        else:   # i.e ROBOTFRAMEWORK
            stmt = 'log   {}'.format(message)

        stmt = indent(stmt, ' ' * self.level * self.indentation)
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
        stmt = indent(stmt, ' ' * self.level * self.indentation)
        return stmt


class DummyStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)
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
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)


class LoopStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)


class PerformerStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)


class VerificationStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)


class SystemStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)
