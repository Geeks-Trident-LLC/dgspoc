import pytest
from os import path

from dgspoc.interpreter import SCRIPTINFO

from dgspoc.interpreter import SetupStatement
from dgspoc.interpreter import CleanupStatement
from dgspoc.interpreter import TeardownStatement
from dgspoc.interpreter import ConnectDataStatement
from dgspoc.interpreter import UseTestCaseStatement
from dgspoc.interpreter import ConnectDeviceStatement
from dgspoc.interpreter import DisconnectStatement
from dgspoc.interpreter import ReleaseDeviceStatement
from dgspoc.interpreter import ReleaseResourceStatement
from dgspoc.interpreter import WaitForStatement

from dgspoc.interpreter import ScriptBuilder

from dgspoc.utils import Misc

from dgspoc.utils import File
from dgspoc.utils import DotObject

fn = path.join(path.dirname(__file__), 'data/interpreter_test_data.yaml')
TESTDATA = File.get_result_from_yaml_file(fn)
TESTDATA = DotObject(TESTDATA)

SCRIPTINFO.enable_testing()


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
        SCRIPTINFO.reset_devices_vars()
        node = SetupStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestConnectDataStatement:
    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.connect_data_statement.case1.data,
                TESTDATA.connect_data_statement.case1.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.connect_data_statement.case1.data,
                TESTDATA.connect_data_statement.case1.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.connect_data_statement.case1.data,
                TESTDATA.connect_data_statement.case1.robotframework,
            ),
        ]
    )
    def test_connect_data_statement(self, framework, indentation,
                                    user_data, expected_result):
        node = ConnectDataStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.connect_data_statement.case2.data,
                TESTDATA.connect_data_statement.case2.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.connect_data_statement.case2.data,
                TESTDATA.connect_data_statement.case2.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.connect_data_statement.case2.data,
                TESTDATA.connect_data_statement.case2.robotframework,
            ),
        ]
    )
    def test_connect_data_statement_and_assign_to_var(
        self, framework, indentation, user_data, expected_result
    ):
        node = ConnectDataStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestUseTestcaseStatement:
    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.use_testcase_statement.case1.data,
                TESTDATA.use_testcase_statement.case1.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.use_testcase_statement.case1.data,
                TESTDATA.use_testcase_statement.case1.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.use_testcase_statement.case1.data,
                TESTDATA.use_testcase_statement.case1.robotframework,
            ),
        ]
    )
    def test_use_testcase_statement(self, framework, indentation,
                                    user_data, expected_result):
        SCRIPTINFO.reset_global_vars()
        node = UseTestCaseStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.use_testcase_statement.case2.data,
                TESTDATA.use_testcase_statement.case2.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.use_testcase_statement.case2.data,
                TESTDATA.use_testcase_statement.case2.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.use_testcase_statement.case2.data,
                TESTDATA.use_testcase_statement.case2.robotframework,
            ),
        ]
    )
    def test_use_testcase_statement_and_assign_to_var(
        self, framework, indentation, user_data, expected_result
    ):
        SCRIPTINFO.reset_global_vars()
        node = UseTestCaseStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestConnectDeviceStatement:
    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.connect_device_statement.case1.data,
                TESTDATA.connect_device_statement.case1.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.connect_device_statement.case1.data,
                TESTDATA.connect_device_statement.case1.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.connect_device_statement.case1.data,
                TESTDATA.connect_device_statement.case1.robotframework,
            ),
        ]
    )
    def test_connect_single_device_with_default_var_name(
        self, framework, indentation, user_data, expected_result
    ):
        SCRIPTINFO.reset_global_vars()
        SCRIPTINFO.reset_devices_vars()
        node = ConnectDeviceStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.connect_device_statement.case2.data,
                TESTDATA.connect_device_statement.case2.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.connect_device_statement.case2.data,
                TESTDATA.connect_device_statement.case2.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.connect_device_statement.case2.data,
                TESTDATA.connect_device_statement.case2.robotframework,
            ),
        ]
    )
    def test_connect_multiple_devices_with_default_var_name(
        self, framework, indentation, user_data, expected_result
    ):
        SCRIPTINFO.reset_global_vars()
        SCRIPTINFO.reset_devices_vars()
        node = ConnectDeviceStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.connect_device_statement.case3.data,
                TESTDATA.connect_device_statement.case3.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.connect_device_statement.case3.data,
                TESTDATA.connect_device_statement.case3.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.connect_device_statement.case3.data,
                TESTDATA.connect_device_statement.case3.robotframework,
            ),
        ]
    )
    def test_connect_devices_with_custom_var_name(
        self, framework, indentation, user_data, expected_result
    ):
        SCRIPTINFO.reset_global_vars()
        SCRIPTINFO.reset_devices_vars()
        node = ConnectDeviceStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.connect_device_statement.case4.data,
                TESTDATA.connect_device_statement.case4.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.connect_device_statement.case4.data,
                TESTDATA.connect_device_statement.case4.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.connect_device_statement.case4.data,
                TESTDATA.connect_device_statement.case4.robotframework,
            ),
        ]
    )
    def test_connect_devices_with_mixing_var_name(
        self, framework, indentation, user_data, expected_result
    ):
        SCRIPTINFO.reset_global_vars()
        SCRIPTINFO.reset_devices_vars()
        node = ConnectDeviceStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.connect_device_statement.case5.data,
                TESTDATA.connect_device_statement.case5.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.connect_device_statement.case5.data,
                TESTDATA.connect_device_statement.case5.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.connect_device_statement.case5.data,
                TESTDATA.connect_device_statement.case5.robotframework,
            ),
        ]
    )
    def test_connect_device_with_other_format(
        self, framework, indentation, user_data, expected_result
    ):
        SCRIPTINFO.reset_global_vars()
        SCRIPTINFO.reset_devices_vars()
        node = ConnectDeviceStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestDisconnectDeviceStatement:
    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.disconnect_device_statement.case1.data,
                TESTDATA.disconnect_device_statement.case1.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.disconnect_device_statement.case1.data,
                TESTDATA.disconnect_device_statement.case1.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.disconnect_device_statement.case1.data,
                TESTDATA.disconnect_device_statement.case1.robotframework,
            ),
        ]
    )
    def test_disconnect_device(
        self, framework, indentation, user_data, expected_result
    ):
        node = DisconnectStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.disconnect_device_statement.case2.data,
                TESTDATA.disconnect_device_statement.case2.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.disconnect_device_statement.case2.data,
                TESTDATA.disconnect_device_statement.case2.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.disconnect_device_statement.case2.data,
                TESTDATA.disconnect_device_statement.case2.robotframework,
            ),
        ]
    )
    def test_disconnect_device_other_format(
        self, framework, indentation, user_data, expected_result
    ):
        node = DisconnectStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestReleaseDeviceStatement:
    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.release_device_statement.case1.data,
                TESTDATA.release_device_statement.case1.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.release_device_statement.case1.data,
                TESTDATA.release_device_statement.case1.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.release_device_statement.case1.data,
                TESTDATA.release_device_statement.case1.robotframework,
            ),
        ]
    )
    def test_release_device(
        self, framework, indentation, user_data, expected_result
    ):
        node = ReleaseDeviceStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestReleaseResourceStatement:
    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.release_resource_statement.case1.data,
                TESTDATA.release_resource_statement.case1.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.release_resource_statement.case1.data,
                TESTDATA.release_resource_statement.case1.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.release_resource_statement.case1.data,
                TESTDATA.release_resource_statement.case1.robotframework,
            ),
        ]
    )
    def test_release_device(
        self, framework, indentation, user_data, expected_result
    ):
        node = ReleaseResourceStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestCleanupStatement:
    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.cleanup_statement.default.data,
                Misc.skip_first_line(TESTDATA.cleanup_statement.default.unittest),
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.cleanup_statement.default.data,
                Misc.skip_first_line(TESTDATA.cleanup_statement.default.pytest),
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.cleanup_statement.default.data,
                Misc.skip_first_line(TESTDATA.cleanup_statement.default.robotframework),
            ),
        ]
    )
    def test_default_cleanup_statement(self, framework, indentation,
                                       user_data, expected_result):
        node = CleanupStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.cleanup_statement.case1.data,
                Misc.skip_first_line(TESTDATA.cleanup_statement.case1.unittest),
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.cleanup_statement.case1.data,
                Misc.skip_first_line(TESTDATA.cleanup_statement.case1.pytest),
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.cleanup_statement.case1.data,
                Misc.skip_first_line(TESTDATA.cleanup_statement.case1.robotframework),
            ),
        ]
    )
    def test_cleanup_with_disconnect_and_release(
        self, framework, indentation, user_data, expected_result
    ):
        node = CleanupStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestTeardownStatement:

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.teardown_statement.default.data,
                Misc.skip_first_line(TESTDATA.teardown_statement.default.unittest),
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.teardown_statement.default.data,
                Misc.skip_first_line(TESTDATA.teardown_statement.default.pytest),
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.teardown_statement.default.data,
                Misc.skip_first_line(TESTDATA.teardown_statement.default.robotframework),
            ),
        ]
    )
    def test_default_teardown_statement(self, framework, indentation,
                                        user_data, expected_result):
        node = TeardownStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.teardown_statement.case1.data,
                Misc.skip_first_line(TESTDATA.teardown_statement.case1.unittest),
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.teardown_statement.case1.data,
                Misc.skip_first_line(TESTDATA.teardown_statement.case1.pytest),
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.teardown_statement.case1.data,
                Misc.skip_first_line(TESTDATA.teardown_statement.case1.robotframework),
            ),
        ]
    )
    def test_teardown_with_disconnect_and_release(
        self, framework, indentation, user_data, expected_result
    ):
        node = CleanupStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestWaitForStatement:
    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.waitfor_statement.case1.data,
                TESTDATA.waitfor_statement.case1.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.waitfor_statement.case1.data,
                TESTDATA.waitfor_statement.case1.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.waitfor_statement.case1.data,
                TESTDATA.waitfor_statement.case1.robotframework,
            ),
        ]
    )
    def test_wait_for_statement_case1(
        self, framework, indentation, user_data, expected_result
    ):
        node = WaitForStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.waitfor_statement.case2.data,
                TESTDATA.waitfor_statement.case2.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.waitfor_statement.case2.data,
                TESTDATA.waitfor_statement.case2.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.waitfor_statement.case2.data,
                TESTDATA.waitfor_statement.case2.robotframework,
            ),
        ]
    )
    def test_wait_for_statement_case2(
        self, framework, indentation, user_data, expected_result
    ):
        node = WaitForStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.waitfor_statement.case3.data,
                TESTDATA.waitfor_statement.case3.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.waitfor_statement.case3.data,
                TESTDATA.waitfor_statement.case3.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.waitfor_statement.case3.data,
                TESTDATA.waitfor_statement.case3.robotframework,
            ),
        ]
    )
    def test_wait_for_statement_case3(
        self, framework, indentation, user_data, expected_result
    ):
        node = WaitForStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.waitfor_statement.case4.data,
                TESTDATA.waitfor_statement.case4.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.waitfor_statement.case4.data,
                TESTDATA.waitfor_statement.case4.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.waitfor_statement.case4.data,
                TESTDATA.waitfor_statement.case4.robotframework,
            ),
        ]
    )
    def test_wait_for_statement_case3(
        self, framework, indentation, user_data, expected_result
    ):
        node = WaitForStatement(user_data, indentation=indentation, framework=framework)
        snippet = node.snippet
        assert snippet == expected_result


class TestScriptBuilder:

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.script_builder.default.data,
                TESTDATA.script_builder.default.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.script_builder.default.data,
                TESTDATA.script_builder.default.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.script_builder.default.data,
                TESTDATA.script_builder.default.robotframework,
            ),
        ]
    )
    def test_default_script_builder(
        self, framework, indentation, user_data, expected_result
    ):
        node = ScriptBuilder(user_data, indentation=indentation, framework=framework)
        test_script = node.testscript
        assert test_script == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_info', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.user_info,
                TESTDATA.script_builder.default_with_user_info.data,
                TESTDATA.script_builder.default_with_user_info.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.user_info,
                TESTDATA.script_builder.default_with_user_info.data,
                TESTDATA.script_builder.default_with_user_info.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.user_info,
                TESTDATA.script_builder.default_with_user_info.data,
                TESTDATA.script_builder.default_with_user_info.robotframework,
            ),
        ]
    )
    def test_default_script_builder_with_user_info(
        self, framework, indentation, user_info, user_data, expected_result
    ):
        node = ScriptBuilder(
            user_data,
            indentation=indentation,
            framework=framework,
            username=user_info.username,
            email=user_info.email,
            company=user_info.company
        )
        test_script = node.testscript
        assert test_script == expected_result

    @pytest.mark.parametrize(
        ('framework', 'indentation', 'user_info', 'user_data', 'expected_result'),
        [
            (
                'unittest',
                TESTDATA.indentation,
                TESTDATA.user_info,
                TESTDATA.script_builder.case1.data,
                TESTDATA.script_builder.case1.unittest,
            ),
            (
                'pytest',
                TESTDATA.indentation,
                TESTDATA.user_info,
                TESTDATA.script_builder.case1.data,
                TESTDATA.script_builder.case1.pytest,
            ),
            (
                'robotframework',
                TESTDATA.indentation,
                TESTDATA.user_info,
                TESTDATA.script_builder.case1.data,
                TESTDATA.script_builder.case1.robotframework,
            ),
        ]
    )
    def test_building_script_case1(
        self, framework, indentation, user_info, user_data, expected_result
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
        test_script = node.testscript
        assert test_script == expected_result
