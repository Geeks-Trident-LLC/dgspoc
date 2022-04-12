"""Module containing the logic for describe-get-system to interpret
user describing problem"""


import re
import operator

from textwrap import indent

from dgspoc.utils import DictObject
from dgspoc.utils import Misc
from dgspoc.utils import File

from dgspoc.constant import FWTYPE

from dgspoc.exceptions import NotImplementedFrameworkError
from dgspoc.exceptions import ComparisonOperatorError


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

        self.spacer_pattern = r'(?P<spacers> *)[^ ].*'

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

    @property
    def is_setup_statement(self):
        pattern = r'setup'
        is_matched = self.is_matched_statement(pattern)
        return is_matched

    @property
    def is_teardown_statement(self):
        pattern = r'cleanup|teardown'
        is_matched = self.is_matched_statement(pattern)
        return is_matched

    @property
    def is_section_statement(self):
        pattern = r'section'
        is_matched = self.is_matched_statement(pattern)
        return is_matched

    @property
    def is_base_statement(self):
        is_base_stmt = self.is_setup_statement
        is_base_stmt |= self.is_section_statement
        is_base_stmt |= self.is_teardown_statement
        return is_base_stmt

    def is_matched_statement(self, pat, data=None):
        data = data or [self.name, self.statement_data]
        lst = data if Misc.is_list(data) else [data]
        is_matched = any(bool(re.match(pat, str(item), re.I)) for item in lst)
        return is_matched

    def prepare(self):
        if self.is_empty:
            self._stmt_data = ''
            self._remaining_data = ''
        else:
            lst = self.data.splitlines()
            for index, line in enumerate(lst):
                line = str(line).rstrip()
                if line.strip():
                    match = re.match(self.spacer_pattern, line)
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

                    if self.is_base_statement:
                        self._level = 0
                        self._spacers = ''

                    return

    def get_next_statement_data(self):
        for line in self.remaining_data.splitlines():
            if line.strip():
                return line
        else:
            return ''

    def has_next_statement(self):
        next_stmt_data = self.get_next_statement_data()
        return next_stmt_data.strip() != ''

    def check_next_statement(self, op):
        op = str(op).strip().lower()
        if op not in ['eq', 'le', 'lt', 'gt', 'ge', 'ne']:
            failure = 'Operator MUST BE eq, ne, le, lt, ge, or gt'
            raise ComparisonOperatorError(failure)

        if not self.has_next_statement():
            return False
        next_stmt_data = self.get_next_statement_data()
        match = re.match(self.spacer_pattern, next_stmt_data)
        spacers = match.group('spacers') if match else ''

        result = getattr(operator, op)(spacers, self._spacers)
        return result

    def is_next_statement_sibling(self):
        result = self.check_next_statement('eq')
        return result

    def is_next_statement_children(self):
        result = self.check_next_statement('gt')
        return result

    def is_next_statement_ancestor(self):
        result = self.check_next_statement('lt')
        return result

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

    def indent_data(self, data, lvl):
        lvl = lvl if self.framework == FWTYPE.ROBOTFRAMEWORK else lvl + 1
        new_data = indent(data, ' ' * lvl * self.indentation)
        return new_data

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
            self.name = 'dummy'
        else:
            self._is_parsed = False


class SetupStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        lst = []

        if self.framework == FWTYPE.UNITTEST:
            lst.append(self.indent_data('def setUp(self)', self.level))
        elif self.framework == FWTYPE.PYTEST:
            lst.append(self.indent_data('def setup_class(self)', self.level))
        else:   # i.e ROBOTFRAMEWORK
            lst.append(self.indent_data('setup', self.level))

        for child in self._children:
            lst.append(self.indent_data(child.snippet, child.level))

        script = '\n'.join(lst)
        return script

    def parse(self):
        if self.is_setup_statement:
            self.name = 'setup'
            self._is_parsed = True
            self.create_child(self)
            if self.is_next_statement_children():
                node = self.create_child(self)
                while node and node.is_next_statement_sibling():
                    self._children.append(node)
                    node = self.create_child(node)
                if self._children:
                    last_child = self._children[-1]
                    self._remaining_data = last_child.remaining_data
                else:
                    kwargs = dict(framework=self.framework, indentation=self.indentation)
                    data = '    dummy_pass - Dummy Setup'
                    dummy_stmt = DummyStatement(data, **kwargs)
                    self._children.append(dummy_stmt)
        else:
            self._is_parsed = False

    def create_child(self, node):
        kwargs = dict(framework=self.framework, indentation=self.indentation)
        next_line = node.get_next_statement_data()

        if node.is_matched_statement('(?i) +connect +data', next_line):
            other = ConnectDataStatement(node.remaining_data, **kwargs)
        elif node.is_matched_statement('(?i) +connect +data', next_line):
            other = UseTestCaseStatement(node.remaining_data, **kwargs)
        elif node.is_matched_statement('(?i) +connect +device', next_line):
            other = ConnectDeviceStatement(node.remaining_data, **kwargs)
        else:
            return None

        other.prev = node
        # node.next = other
        if node.is_next_statement_children():
            other.parent = node
        else:
            other.parent = node.prev.parent
        return node


class ConnectDataStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)
        self.var_name = ''
        self.test_resource_reference = ''
        self.parse()

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        if self.framework == FWTYPE.ROBOTFRAMEWORK:
            fmt = "${%s}=   connect data   filename='%s'\nset global variable   %s"
            stmt = fmt.format(self.var_name, self.test_resource_reference, self.var_name)
        else:
            fmt = "self.%s = ta.connect_data(filename='%s')"
            stmt = fmt.format(self.var_name, self.test_resource_reference)

        stmt = self.indent_data(stmt, self.level)

        return stmt

    def parse(self):
        pattern = r'(?i) +connect +data +(?P<test_rsrc_ref>\S+)( +as (?P<var>[a-z]\w*))? *$'
        match = re.match(pattern, self.statement_data)
        if match:
            test_rsrc_ref = match.group('test_rsrc_ref')
            var_name = match.group('var') or 'test_resource'

            yaml_obj = File.get_result_from_yaml_file(test_rsrc_ref)
            if 'testcases' in yaml_obj:
                self.var_name = var_name
                self.test_resource_reference = test_rsrc_ref
                SCRIPTINFO.update(yaml_obj.get('testcases'))
                variables = SCRIPTINFO.get('variables', DictObject())
                SCRIPTINFO.variables = variables
                variables.test_resource_var = self.var_name
                self.name = 'connect_data'
                self._is_parsed = True
        else:
            self._is_parsed = False


class UseTestCaseStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)
        self.var_name = ''
        self.test_name = ''

    @property
    def snippet(self):
        if not self.is_parsed:
            return ''

        test_resource_var = SCRIPTINFO.variables.test_resource_var  # noqa

        if self.framework == FWTYPE.ROBOTFRAMEWORK:
            fmt = "${%s}=  use testcase   %s  device='%s'\nset global variable   %s"
            stmt = fmt.format(
                self.var_name, test_resource_var, self.test_name, self.var_name
            )
        else:
            fmt = "self.%s = ta.use_testcase(self.%s, device='%s')"
            stmt = fmt.format(
                self.var_name, test_resource_var, self.test_name
            )

        stmt = self.indent_data(stmt, self.level)

        return stmt

    def parse(self):
        pattern = r'(?i) +use +testcase +(?P<test_name>\S+)( +as (?P<var>[a-z]\w*))? *$'
        match = re.match(pattern, self.statement_data)
        if match:
            test_name = match.group('test_name')
            var_name = match.group('var') or 'test_data'

            if test_name in SCRIPTINFO:
                self.var_name = var_name
                self.test_name = test_name

                variables = SCRIPTINFO.get('variables', DictObject())
                SCRIPTINFO.variables = variables
                SCRIPTINFO.variables.test_data_var = self.var_name
                self.name = 'use_testcase'
                self._is_parsed = True
        else:
            self._is_parsed = False


class ConnectDeviceStatement(Statement):
    def __init__(self, data, parent=None, framework='', indentation=4):
        super().__init__(data, parent=parent, framework=framework,
                         indentation=indentation)


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
