import pytest

from dgspoc.utils import File
from dgspoc.utils import MiscOutput

from . import ReformatOutput

TESTDATA = File.get_result_from_yaml_file(
    'data/console_test_cli_data.yaml',
    base_dir=__file__,
    dot_datatype=True,
    var_substitution=True,
    root_var_name='self'
)


class TestConsoleTestCommandLineUsage:
    """Note: the comment in pytest.mark.parametrize should work as same as
    the previous command line"""

    @pytest.mark.parametrize(
        'cmdline',
        [
            'dgs test --help',
            # 'dgs test usage',
        ]
    )
    def test_console_test_cli_help(self, cmdline):
        result = MiscOutput.execute_shell_command(cmdline)

        assert result.is_success
        assert 'dgs test usage' in result.output
        assert ' --adaptor ADAPTOR ' in result.output
        assert ' --action ACTION ' in result.output
        assert ' -h, --help ' in result.output
        assert 'dgs test operands [options]' in result.output
        assert 'dgs test example ' in result.output


class TestConsoleTestCommandLineUsingUnrealDevice:

    def setup_class(self):      # noqa
        result = MiscOutput.execute_shell_command(TESTDATA.created_template_cmdline)
        assert result.is_success, 'failed to create template at setup'

        result = MiscOutput.execute_shell_command(TESTDATA.connect_cmdline)
        if result.is_success:
            self.is_ready = True
            MiscOutput.execute_shell_command(TESTDATA.release_cmdline)
        else:
            self.is_ready = False
            assert self.is_ready, 'This test needs gtunrealdevice package (Installation: pip install gtunrealdevice)'

    def teardown_class(self):   # noqa
        result = MiscOutput.execute_shell_command(TESTDATA.cleared_template_cmdline)
        assert result.is_success, 'failed to clean template at teardown'

    @pytest.mark.parametrize(
        ('cmdline', 'expected_result'),
        [
            (TESTDATA.case1.cmdline, TESTDATA.case1.expected_result),
            (TESTDATA.case2.cmdline, TESTDATA.case2.expected_result),
            (TESTDATA.case3.cmdline, TESTDATA.case3.expected_result),
            (TESTDATA.case4.cmdline, TESTDATA.case4.expected_result),
            (TESTDATA.case5.cmdline, TESTDATA.case5.expected_result),
            (TESTDATA.case6.cmdline, TESTDATA.case6.expected_result),
            (TESTDATA.case7.cmdline, TESTDATA.case7.expected_result),
            (TESTDATA.case8.cmdline, TESTDATA.case8.expected_result),
            (TESTDATA.case9.cmdline, TESTDATA.case9.expected_result),
            (TESTDATA.case10.cmdline, TESTDATA.case10.expected_result),
        ]
    )
    def test_or_verify(self, cmdline, expected_result):
        result = MiscOutput.execute_shell_command(cmdline)
        reformat_result = ReformatOutput(result.output)
        assert result.is_success
        assert reformat_result == expected_result
