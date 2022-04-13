import pytest
from os import path


from dgspoc.interpreter import SetupStatement
from dgspoc.interpreter import SCRIPTINFO

from dgspoc.utils import Misc

from dgspoc.utils import File
from dgspoc.utils import DotObject

fn = path.join(path.dirname(__file__), 'data/interpreter_test_data.yaml')
TESTDATA = File.get_result_from_yaml_file(fn)
TESTDATA = DotObject(TESTDATA)


class TestSetupStatement:
    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.setup_statement.default.data,
                Misc.skip_first_line(TESTDATA.setup_statement.default.unittest),
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.setup_statement.default.data,
                Misc.skip_first_line(TESTDATA.setup_statement.default.pytest),
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.setup_statement.default.data,
                Misc.skip_first_line(TESTDATA.setup_statement.default.robotframework),
            ),
        ]
    )
    def test_default_setup_statement(self, framework, indentation,
                                     user_data, expected_result):
        node = SetupStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.setup_statement.case1.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case1.unittest),
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.setup_statement.case1.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case1.pytest),
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.setup_statement.case1.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case1.robotframework),
            ),
        ]
    )
    def test_setup_connect_data(self, framework, indentation,
                                user_data, expected_result):
        node = SetupStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.setup_statement.case2.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case2.unittest),
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.setup_statement.case2.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case2.pytest),
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.setup_statement.case2.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case2.robotframework),
            ),
        ]
    )
    def test_setup_connect_data_and_use_testcase(
        self, framework, indentation, user_data, expected_result
    ):
        node = SetupStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.setup_statement.case3.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case3.unittest),
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.setup_statement.case3.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case3.pytest),
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.setup_statement.case3.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case3.robotframework),
            ),
        ]
    )
    def test_setup_connect_data_and_use_testcase_and_connect_device(
        self, framework, indentation, user_data, expected_result
    ):
        SCRIPTINFO.clear_devices_vars()
        node = SetupStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result
