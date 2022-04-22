import pytest
from os import path

from dgspoc.constant import FWTYPE

from dgspoc.interpreter import SCRIPTINFO

from dgspoc.interpreter import DummyStatement
from dgspoc.interpreter import SetupStatement
from dgspoc.interpreter import TeardownStatement
from dgspoc.interpreter import SectionStatement
from dgspoc.interpreter import ConnectDataStatement
from dgspoc.interpreter import UseTestCaseStatement
from dgspoc.interpreter import ConnectDeviceStatement
from dgspoc.interpreter import DisconnectStatement
from dgspoc.interpreter import ReleaseDeviceStatement
from dgspoc.interpreter import ReleaseResourceStatement
from dgspoc.interpreter import LoopStatement
from dgspoc.interpreter import PerformerStatement
from dgspoc.interpreter import VerificationStatement
from dgspoc.interpreter import WaitForStatement

from dgspoc.interpreter import ScriptBuilder

from dgspoc.utils import Misc

from dgspoc.utils import File
from dgspoc.utils import DotObject

fn = path.join(path.dirname(__file__), 'data/interpreter_test_data.yaml')
TESTDATA = File.get_result_from_yaml_file(fn)
TESTDATA = DotObject(TESTDATA)

SCRIPTINFO.enable_testing()

indentation = TESTDATA.indentation
user_info = TESTDATA.user_info


class TestDummyStatement:
    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.dummy_statement.case1.data,
                TESTDATA.dummy_statement.case1.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.dummy_statement.case1.data,
                TESTDATA.dummy_statement.case1.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.dummy_statement.case1.data,
                TESTDATA.dummy_statement.case1.robotframework,
            ),
        ]
    )
    def test_dummy_statement_case1(self, framework, user_data, expected_result):
        node = DummyStatement(user_data, indentation=indentation,
                              framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.dummy_statement.case2.data,
                TESTDATA.dummy_statement.case2.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.dummy_statement.case2.data,
                TESTDATA.dummy_statement.case2.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.dummy_statement.case2.data,
                TESTDATA.dummy_statement.case2.robotframework,
            ),
        ]
    )
    def test_dummy_statement_case2(self, framework, user_data, expected_result):
        node = DummyStatement(user_data, indentation=indentation,
                              framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.dummy_statement.case3.data,
                TESTDATA.dummy_statement.case3.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.dummy_statement.case3.data,
                TESTDATA.dummy_statement.case3.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.dummy_statement.case3.data,
                TESTDATA.dummy_statement.case3.robotframework,
            ),
        ]
    )
    def test_dummy_statement_case3(self, framework, user_data, expected_result):
        node = DummyStatement(user_data, indentation=indentation,
                              framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestSetupStatement:
    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.setup_statement.default.data,
                Misc.skip_first_line(TESTDATA.setup_statement.default.unittest),
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.setup_statement.default.data,
                Misc.skip_first_line(TESTDATA.setup_statement.default.pytest),
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.setup_statement.default.data,
                Misc.skip_first_line(TESTDATA.setup_statement.default.robotframework),
            ),
        ]
    )
    def test_default_setup_statement(self, framework, user_data, expected_result):
        node = SetupStatement(user_data, indentation=indentation,
                              framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.setup_statement.case1.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case1.unittest),
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.setup_statement.case1.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case1.pytest),
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.setup_statement.case1.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case1.robotframework),
            ),
        ]
    )
    def test_setup_connect_data(self, framework, user_data, expected_result):
        node = SetupStatement(user_data, indentation=indentation,
                              framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.setup_statement.case2.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case2.unittest),
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.setup_statement.case2.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case2.pytest),
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.setup_statement.case2.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case2.robotframework),
            ),
        ]
    )
    def test_setup_connect_data_and_use_testcase(self, framework, user_data, expected_result):
        node = SetupStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.setup_statement.case3.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case3.unittest),
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.setup_statement.case3.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case3.pytest),
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.setup_statement.case3.data,
                Misc.skip_first_line(TESTDATA.setup_statement.case3.robotframework),
            ),
        ]
    )
    def test_setup_connect_data_and_use_testcase_and_connect_device(
        self, framework, user_data, expected_result
    ):
        SCRIPTINFO.reset_devices_vars()
        node = SetupStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestConnectDataStatement:
    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.connect_data_statement.case1.data,
                TESTDATA.connect_data_statement.case1.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.connect_data_statement.case1.data,
                TESTDATA.connect_data_statement.case1.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.connect_data_statement.case1.data,
                TESTDATA.connect_data_statement.case1.robotframework,
            ),
        ]
    )
    def test_connect_data_statement(self, framework, user_data, expected_result):
        node = ConnectDataStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.connect_data_statement.case2.data,
                TESTDATA.connect_data_statement.case2.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.connect_data_statement.case2.data,
                TESTDATA.connect_data_statement.case2.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.connect_data_statement.case2.data,
                TESTDATA.connect_data_statement.case2.robotframework,
            ),
        ]
    )
    def test_connect_data_statement_and_assign_to_var(
        self, framework, user_data, expected_result
    ):
        node = ConnectDataStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestUseTestcaseStatement:
    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.use_testcase_statement.case1.data,
                TESTDATA.use_testcase_statement.case1.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.use_testcase_statement.case1.data,
                TESTDATA.use_testcase_statement.case1.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.use_testcase_statement.case1.data,
                TESTDATA.use_testcase_statement.case1.robotframework,
            ),
        ]
    )
    def test_use_testcase_statement(self, framework, user_data, expected_result):
        SCRIPTINFO.reset_global_vars()
        node = UseTestCaseStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.use_testcase_statement.case2.data,
                TESTDATA.use_testcase_statement.case2.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.use_testcase_statement.case2.data,
                TESTDATA.use_testcase_statement.case2.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.use_testcase_statement.case2.data,
                TESTDATA.use_testcase_statement.case2.robotframework,
            ),
        ]
    )
    def test_use_testcase_statement_and_assign_to_var(
        self, framework, user_data, expected_result
    ):
        SCRIPTINFO.reset_global_vars()
        node = UseTestCaseStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestConnectDeviceStatement:
    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.connect_device_statement.case1.data,
                TESTDATA.connect_device_statement.case1.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.connect_device_statement.case1.data,
                TESTDATA.connect_device_statement.case1.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.connect_device_statement.case1.data,
                TESTDATA.connect_device_statement.case1.robotframework,
            ),
        ]
    )
    def test_connect_single_device_with_default_var_name(
        self, framework, user_data, expected_result
    ):
        SCRIPTINFO.reset_global_vars()
        SCRIPTINFO.reset_devices_vars()
        node = ConnectDeviceStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.connect_device_statement.case2.data,
                TESTDATA.connect_device_statement.case2.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.connect_device_statement.case2.data,
                TESTDATA.connect_device_statement.case2.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.connect_device_statement.case2.data,
                TESTDATA.connect_device_statement.case2.robotframework,
            ),
        ]
    )
    def test_connect_multiple_devices_with_default_var_name(
        self, framework, user_data, expected_result
    ):
        SCRIPTINFO.reset_global_vars()
        SCRIPTINFO.reset_devices_vars()
        node = ConnectDeviceStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.connect_device_statement.case3.data,
                TESTDATA.connect_device_statement.case3.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.connect_device_statement.case3.data,
                TESTDATA.connect_device_statement.case3.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.connect_device_statement.case3.data,
                TESTDATA.connect_device_statement.case3.robotframework,
            ),
        ]
    )
    def test_connect_devices_with_custom_var_name(self, framework, user_data, expected_result):
        SCRIPTINFO.reset_global_vars()
        SCRIPTINFO.reset_devices_vars()
        node = ConnectDeviceStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.connect_device_statement.case4.data,
                TESTDATA.connect_device_statement.case4.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.connect_device_statement.case4.data,
                TESTDATA.connect_device_statement.case4.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.connect_device_statement.case4.data,
                TESTDATA.connect_device_statement.case4.robotframework,
            ),
        ]
    )
    def test_connect_devices_with_mixing_var_name(self, framework, user_data, expected_result):
        SCRIPTINFO.reset_global_vars()
        SCRIPTINFO.reset_devices_vars()
        node = ConnectDeviceStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.connect_device_statement.case5.data,
                TESTDATA.connect_device_statement.case5.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.connect_device_statement.case5.data,
                TESTDATA.connect_device_statement.case5.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.connect_device_statement.case5.data,
                TESTDATA.connect_device_statement.case5.robotframework,
            ),
        ]
    )
    def test_connect_device_with_other_format(self, framework, user_data, expected_result):
        SCRIPTINFO.reset_global_vars()
        SCRIPTINFO.reset_devices_vars()
        node = ConnectDeviceStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestDisconnectDeviceStatement:
    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.disconnect_device_statement.case1.data,
                TESTDATA.disconnect_device_statement.case1.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.disconnect_device_statement.case1.data,
                TESTDATA.disconnect_device_statement.case1.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.disconnect_device_statement.case1.data,
                TESTDATA.disconnect_device_statement.case1.robotframework,
            ),
        ]
    )
    def test_disconnect_device(self, framework, user_data, expected_result):
        node = DisconnectStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.disconnect_device_statement.case2.data,
                TESTDATA.disconnect_device_statement.case2.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.disconnect_device_statement.case2.data,
                TESTDATA.disconnect_device_statement.case2.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.disconnect_device_statement.case2.data,
                TESTDATA.disconnect_device_statement.case2.robotframework,
            ),
        ]
    )
    def test_disconnect_device_other_format(self, framework, user_data, expected_result):
        node = DisconnectStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestReleaseDeviceStatement:
    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.release_device_statement.case1.data,
                TESTDATA.release_device_statement.case1.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.release_device_statement.case1.data,
                TESTDATA.release_device_statement.case1.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.release_device_statement.case1.data,
                TESTDATA.release_device_statement.case1.robotframework,
            ),
        ]
    )
    def test_release_device(self, framework, user_data, expected_result):
        node = ReleaseDeviceStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestReleaseResourceStatement:
    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.release_resource_statement.case1.data,
                TESTDATA.release_resource_statement.case1.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.release_resource_statement.case1.data,
                TESTDATA.release_resource_statement.case1.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.release_resource_statement.case1.data,
                TESTDATA.release_resource_statement.case1.robotframework,
            ),
        ]
    )
    def test_release_device(self, framework, user_data, expected_result):
        node = ReleaseResourceStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestTeardownStatement:

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.teardown_statement.default.data,
                Misc.skip_first_line(TESTDATA.teardown_statement.default.unittest),
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.teardown_statement.default.data,
                Misc.skip_first_line(TESTDATA.teardown_statement.default.pytest),
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.teardown_statement.default.data,
                Misc.skip_first_line(TESTDATA.teardown_statement.default.robotframework),
            ),
        ]
    )
    def test_default_teardown_statement(self, framework, user_data, expected_result):
        node = TeardownStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.teardown_statement.case1.data,
                Misc.skip_first_line(TESTDATA.teardown_statement.case1.unittest),
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.teardown_statement.case1.data,
                Misc.skip_first_line(TESTDATA.teardown_statement.case1.pytest),
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.teardown_statement.case1.data,
                Misc.skip_first_line(TESTDATA.teardown_statement.case1.robotframework),
            ),
        ]
    )
    def test_teardown_with_disconnect_and_release(self, framework, user_data, expected_result):
        node = TeardownStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestSectionStatement:

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.section_statement.default.data,
                Misc.skip_first_line(TESTDATA.section_statement.default.unittest),
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.section_statement.default.data,
                Misc.skip_first_line(TESTDATA.section_statement.default.pytest),
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.section_statement.default.data,
                Misc.skip_first_line(TESTDATA.section_statement.default.robotframework),
            ),
        ]
    )
    def test_default_section_statement(self, framework, user_data, expected_result):
        node = SectionStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.section_statement.case1.data,
                Misc.skip_first_line(TESTDATA.section_statement.case1.unittest),
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.section_statement.case1.data,
                Misc.skip_first_line(TESTDATA.section_statement.case1.pytest),
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.section_statement.case1.data,
                Misc.skip_first_line(TESTDATA.section_statement.case1.robotframework),
            ),
        ]
    )
    def test_section_statement_case1(self, framework, user_data, expected_result):
        node = SectionStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.section_statement.case2.data,
                Misc.skip_first_line(TESTDATA.section_statement.case2.unittest),
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.section_statement.case2.data,
                Misc.skip_first_line(TESTDATA.section_statement.case2.pytest),
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.section_statement.case2.data,
                Misc.skip_first_line(TESTDATA.section_statement.case2.robotframework),
            ),
        ]
    )
    def test_section_statement_case2(self, framework, user_data, expected_result):
        node = SectionStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestLoopStatement:
    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.loop_statement.case1.data,
                TESTDATA.loop_statement.case1.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.loop_statement.case1.data,
                TESTDATA.loop_statement.case1.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.loop_statement.case1.data,
                TESTDATA.loop_statement.case1.robotframework,
            ),
        ]
    )
    def test_loop_statement_case1(self, framework, user_data, expected_result):
        node = LoopStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.loop_statement.case2.data,
                TESTDATA.loop_statement.case2.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.loop_statement.case2.data,
                TESTDATA.loop_statement.case2.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.loop_statement.case2.data,
                TESTDATA.loop_statement.case2.robotframework,
            ),
        ]
    )
    def test_loop_statement_case2(self, framework, user_data, expected_result):
        node = LoopStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.loop_statement.case3.data,
                TESTDATA.loop_statement.case3.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.loop_statement.case3.data,
                TESTDATA.loop_statement.case3.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.loop_statement.case3.data,
                TESTDATA.loop_statement.case3.robotframework,
            ),
        ]
    )
    def test_loop_statement_case3(self, framework, user_data, expected_result):
        node = LoopStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.loop_statement.case4.data,
                TESTDATA.loop_statement.case4.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.loop_statement.case4.data,
                TESTDATA.loop_statement.case4.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.loop_statement.case4.data,
                TESTDATA.loop_statement.case4.robotframework,
            ),
        ]
    )
    def test_loop_statement_case4(self, framework, user_data, expected_result):
        node = LoopStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.loop_statement.case5.data,
                TESTDATA.loop_statement.case5.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.loop_statement.case5.data,
                TESTDATA.loop_statement.case5.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.loop_statement.case5.data,
                TESTDATA.loop_statement.case5.robotframework,
            ),
        ]
    )
    def test_loop_statement_case5(self, framework, user_data, expected_result):
        node = LoopStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestPerformerStatement:
    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.performer_statement.case1.data,
                TESTDATA.performer_statement.case1.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.performer_statement.case1.data,
                TESTDATA.performer_statement.case1.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.performer_statement.case1.data,
                TESTDATA.performer_statement.case1.robotframework,
            ),
        ]
    )
    def test_performer_statement_case1(self, framework, user_data, expected_result):
        node = PerformerStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.performer_statement.case2.data,
                TESTDATA.performer_statement.case2.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.performer_statement.case2.data,
                TESTDATA.performer_statement.case2.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.performer_statement.case2.data,
                TESTDATA.performer_statement.case2.robotframework,
            ),
        ]
    )
    def test_performer_statement_case2(self, framework, user_data, expected_result):
        node = PerformerStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.performer_statement.case3.data,
                TESTDATA.performer_statement.case3.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.performer_statement.case3.data,
                TESTDATA.performer_statement.case3.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.performer_statement.case3.data,
                TESTDATA.performer_statement.case3.robotframework,
            ),
        ]
    )
    def test_performer_statement_case3(self, framework, user_data, expected_result):
        node = PerformerStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.performer_statement.case4.data,
                TESTDATA.performer_statement.case4.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.performer_statement.case4.data,
                TESTDATA.performer_statement.case4.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.performer_statement.case4.data,
                TESTDATA.performer_statement.case4.robotframework,
            ),
        ]
    )
    def test_performer_statement_case4(self, framework, user_data, expected_result):
        node = PerformerStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestVerificationStatement:
    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.verification_statement.case1.data,
                TESTDATA.verification_statement.case1.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.verification_statement.case1.data,
                TESTDATA.verification_statement.case1.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.verification_statement.case1.data,
                TESTDATA.verification_statement.case1.robotframework,
            ),
        ]
    )
    def test_verification_statement_case1(self, framework, user_data, expected_result):
        node = VerificationStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.verification_statement.case2.data,
                TESTDATA.verification_statement.case2.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.verification_statement.case2.data,
                TESTDATA.verification_statement.case2.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.verification_statement.case2.data,
                TESTDATA.verification_statement.case2.robotframework,
            ),
        ]
    )
    def test_verification_statement_case2(self, framework, user_data, expected_result):
        node = VerificationStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestWaitForStatement:
    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.waitfor_statement.case1.data,
                TESTDATA.waitfor_statement.case1.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.waitfor_statement.case1.data,
                TESTDATA.waitfor_statement.case1.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.waitfor_statement.case1.data,
                TESTDATA.waitfor_statement.case1.robotframework,
            ),
        ]
    )
    def test_wait_for_statement_case1(self, framework, user_data, expected_result):
        node = WaitForStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.waitfor_statement.case2.data,
                TESTDATA.waitfor_statement.case2.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.waitfor_statement.case2.data,
                TESTDATA.waitfor_statement.case2.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.waitfor_statement.case2.data,
                TESTDATA.waitfor_statement.case2.robotframework,
            ),
        ]
    )
    def test_wait_for_statement_case2(self, framework, user_data, expected_result):
        node = WaitForStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.waitfor_statement.case3.data,
                TESTDATA.waitfor_statement.case3.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.waitfor_statement.case3.data,
                TESTDATA.waitfor_statement.case3.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.waitfor_statement.case3.data,
                TESTDATA.waitfor_statement.case3.robotframework,
            ),
        ]
    )
    def test_wait_for_statement_case3(self, framework, user_data, expected_result):
        node = WaitForStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.waitfor_statement.case4.data,
                TESTDATA.waitfor_statement.case4.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.waitfor_statement.case4.data,
                TESTDATA.waitfor_statement.case4.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.waitfor_statement.case4.data,
                TESTDATA.waitfor_statement.case4.robotframework,
            ),
        ]
    )
    def test_wait_for_statement_case3(self, framework, user_data, expected_result):
        node = WaitForStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestScriptBuilder:

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.script_builder.default.data,
                TESTDATA.script_builder.default.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.script_builder.default.data,
                TESTDATA.script_builder.default.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.script_builder.default.data,
                TESTDATA.script_builder.default.robotframework,
            ),
        ]
    )
    def test_default_script_builder(self, framework, user_data, expected_result):
        node = ScriptBuilder(user_data, indentation=indentation, framework=framework)
        test_script = node.testscript.strip()
        assert test_script == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.script_builder.default_with_user_info.data,
                TESTDATA.script_builder.default_with_user_info.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.script_builder.default_with_user_info.data,
                TESTDATA.script_builder.default_with_user_info.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.script_builder.default_with_user_info.data,
                TESTDATA.script_builder.default_with_user_info.robotframework,
            ),
        ]
    )
    def test_default_script_builder_with_user_info(
            self, framework, user_data, expected_result
    ):
        node = ScriptBuilder(
            user_data,
            indentation=indentation,
            framework=framework,
            username=user_info.username,
            email=user_info.email,
            company=user_info.company
        )
        test_script = node.testscript.strip()
        assert test_script == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.script_builder.case1.data,
                TESTDATA.script_builder.case1.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.script_builder.case1.data,
                TESTDATA.script_builder.case1.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.script_builder.case1.data,
                TESTDATA.script_builder.case1.robotframework,
            ),
        ]
    )
    def test_building_script_case1(
        self, framework, user_data, expected_result
    ):
        SCRIPTINFO.reset_global_vars()
        SCRIPTINFO.reset_devices_vars()
        node = ScriptBuilder(
            user_data,
            indentation=indentation,
            framework=framework,
            username=user_info.username,
            email=user_info.email,
            company=user_info.company
        )
        test_script = node.testscript.strip()
        assert test_script == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.script_builder.case2.data,
                TESTDATA.script_builder.case2.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.script_builder.case2.data,
                TESTDATA.script_builder.case2.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.script_builder.case2.data,
                TESTDATA.script_builder.case2.robotframework,
            ),
        ]
    )
    def test_building_script_case2(
        self, framework, user_data, expected_result
    ):
        SCRIPTINFO.reset_global_vars()
        SCRIPTINFO.reset_devices_vars()
        SCRIPTINFO.load_testing_data()
        node = ScriptBuilder(
            user_data,
            indentation=indentation,
            framework=framework,
            username=user_info.username,
            email=user_info.email,
            company=user_info.company
        )
        test_script = node.testscript.strip()
        assert test_script == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.script_builder.case3.data,
                TESTDATA.script_builder.case3.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.script_builder.case3.data,
                TESTDATA.script_builder.case3.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.script_builder.case3.data,
                TESTDATA.script_builder.case3.robotframework,
            ),
        ]
    )
    def test_building_script_case3(self, framework, user_data, expected_result):
        SCRIPTINFO.reset_global_vars()
        SCRIPTINFO.reset_devices_vars()
        SCRIPTINFO.load_testing_data()
        node = ScriptBuilder(
            user_data,
            indentation=indentation,
            framework=framework,
            username=user_info.username,
            email=user_info.email,
            company=user_info.company
        )
        test_script = node.testscript.strip()
        assert test_script == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.script_builder.case4.data,
                TESTDATA.script_builder.case4.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.script_builder.case4.data,
                TESTDATA.script_builder.case4.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.script_builder.case4.data,
                TESTDATA.script_builder.case4.robotframework,
            ),
        ]
    )
    def test_building_script_case4(self, framework, user_data, expected_result):
        SCRIPTINFO.reset_global_vars()
        SCRIPTINFO.reset_devices_vars()
        SCRIPTINFO.load_testing_data()
        node = ScriptBuilder(
            user_data,
            indentation=indentation,
            framework=framework,
            username=user_info.username,
            email=user_info.email,
            company=user_info.company
        )
        test_script = node.testscript.strip()
        assert test_script == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.script_builder.case5.data,
                TESTDATA.script_builder.case5.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.script_builder.case5.data,
                TESTDATA.script_builder.case5.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.script_builder.case5.data,
                TESTDATA.script_builder.case5.robotframework,
            ),
        ]
    )
    def test_building_script_case5(self, framework, user_data, expected_result):
        SCRIPTINFO.reset_global_vars()
        SCRIPTINFO.reset_devices_vars()
        SCRIPTINFO.load_testing_data()
        node = ScriptBuilder(
            user_data,
            indentation=indentation,
            framework=framework,
            username=user_info.username,
            email=user_info.email,
            company=user_info.company
        )
        test_script = node.testscript.strip()
        assert test_script == expected_result

    @pytest.mark.parametrize(
        ('framework', 'user_data', 'expected_result'),
        [
            (
                FWTYPE.UNITTEST,
                TESTDATA.script_builder.case6.data,
                TESTDATA.script_builder.case6.unittest,
            ),
            (
                FWTYPE.PYTEST,
                TESTDATA.script_builder.case6.data,
                TESTDATA.script_builder.case6.pytest,
            ),
            (
                FWTYPE.ROBOTFRAMEWORK,
                TESTDATA.script_builder.case6.data,
                TESTDATA.script_builder.case6.robotframework,
            ),
        ]
    )
    def test_building_script_case6(self, framework, user_data, expected_result):
        SCRIPTINFO.reset_global_vars()
        SCRIPTINFO.reset_devices_vars()
        SCRIPTINFO.load_testing_data()
        node = ScriptBuilder(
            user_data,
            indentation=indentation,
            framework=framework,
            username=user_info.username,
            email=user_info.email,
            company=user_info.company,
            is_logger=True
        )
        test_script = node.testscript.strip()
        assert test_script == expected_result
