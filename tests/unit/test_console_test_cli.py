import pytest

from dgspoc.utils import File
from dgspoc.utils import MiscOutput

from . import ReformatOutput

TESTDATA = File.get_result_from_yaml_file(
    'data/console_test_data.yaml',
    base_dir=__file__,
    dot_datatype=True,
    var_substitution=True,
    root_var_name='self'
)


class TestConsoleTestCommandLine:
    """Note: the comment in pytest.mark.parametrize should work as same as
    the previous command line"""

    def setup_class(self):      # noqa
        result = MiscOutput.execute_shell_command(TESTDATA.created_template_cmdline)
        assert result.is_success

    def teardown_class(self):   # noqa
        result = MiscOutput.execute_shell_command(TESTDATA.cleared_template_cmdline)
        assert result.is_success

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

    @pytest.mark.parametrize(
        ('cmdline', 'expected_result'),
        [
            (TESTDATA.case1.cmdline, TESTDATA.case1.expected_result),
            (TESTDATA.case2.cmdline, TESTDATA.case2.expected_result),
            (TESTDATA.case3.cmdline, TESTDATA.case3.expected_result),
        ]
    )
    def test_or_verify(self, cmdline, expected_result):
        result = MiscOutput.execute_shell_command(cmdline)
        reformat_result = ReformatOutput(result.output)
        assert result.is_success
        assert reformat_result == expected_result


