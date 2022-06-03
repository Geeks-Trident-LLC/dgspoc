import pytest

from dgspoc.utils import File
from dgspoc.utils import MiscOutput

from . import ReformatOutput
from . import is_py36_or_py37

TESTDATA = File.get_result_from_yaml_file(
    'data/console_test_cli_data.yaml',
    base_dir=__file__,
    dot_datatype=True,
    var_substitution=True,
    root_var_name='self'
)

base_dir = File.get_dir(__file__)
template_filename = File.get_path(base_dir, 'data/show_modules_template.textfsm')
text_output_filename = File.get_path(base_dir, 'data/show_modules_output.txt')
csv_output_filename = File.get_path(base_dir, 'data/show_modules_csv_output.txt')
json_output_filename = File.get_path(base_dir, 'data/show_modules_json_output.txt')


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
        ]
    )
    def test_or_verify(self, cmdline, expected_result):
        result = MiscOutput.execute_shell_command(cmdline)
        reformat_result = ReformatOutput(result.output, everything=True)

        assert result.is_success
        assert reformat_result.strip() == expected_result


class TestConsoleTestCommandLineUsingFile:
    @pytest.mark.parametrize(
        ('cmdline', 'expected_result'),
        [
            (TESTDATA.case1_using_file_syntax1.fmt % text_output_filename, TESTDATA.case1_using_file_syntax1.expected_result),   # noqa
            (TESTDATA.case1_using_file_syntax2.fmt % text_output_filename, TESTDATA.case1_using_file_syntax2.expected_result),  # noqa
            (TESTDATA.case1_using_file_syntax3.fmt % text_output_filename, TESTDATA.case1_using_file_syntax3.expected_result),  # noqa
            (TESTDATA.case1_using_file_syntax4.fmt % text_output_filename, TESTDATA.case1_using_file_syntax4.expected_result),  # noqa
            (TESTDATA.case1_using_file_syntax5.fmt % text_output_filename, TESTDATA.case1_using_file_syntax5.expected_result),  # noqa

            (TESTDATA.case3_using_file_scenario1.fmt % (csv_output_filename), TESTDATA.case3_using_file_scenario1.expected_result_for_py36_py37 if is_py36_or_py37() else TESTDATA.case3_using_file_scenario1.expected_result),  # noqa
            (TESTDATA.case3_using_file_scenario2.fmt % (csv_output_filename), TESTDATA.case3_using_file_scenario2.expected_result_for_py36_py37 if is_py36_or_py37() else TESTDATA.case3_using_file_scenario2.expected_result),  # noqa
            (TESTDATA.case3_using_file_scenario3.fmt % (csv_output_filename), TESTDATA.case3_using_file_scenario3.expected_result),  # noqa

            (TESTDATA.case4_using_file_scenario1.fmt % (json_output_filename), TESTDATA.case4_using_file_scenario1.expected_result),  # noqa
            (TESTDATA.case4_using_file_scenario2.fmt % (json_output_filename), TESTDATA.case4_using_file_scenario2.expected_result),  # noqa

            (TESTDATA.case5_using_file_scenario1.fmt % (text_output_filename, template_filename), TESTDATA.case5_using_file_scenario1.expected_result),  # noqa
            (TESTDATA.case5_using_file_scenario2.fmt % (text_output_filename, template_filename), TESTDATA.case5_using_file_scenario2.expected_result),  # noqa

            (TESTDATA.case6_using_file_scenario1.fmt % (text_output_filename, template_filename), TESTDATA.case6_using_file_scenario1.expected_result),  # noqa
            (TESTDATA.case6_using_file_scenario2.fmt % (text_output_filename, template_filename), TESTDATA.case6_using_file_scenario2.expected_result),  # noqa
            (TESTDATA.case6_using_file_scenario3.fmt % (text_output_filename, template_filename), TESTDATA.case6_using_file_scenario3.expected_result),  # noqa
            (TESTDATA.case6_using_file_scenario4.fmt % (text_output_filename, template_filename), TESTDATA.case6_using_file_scenario4.expected_result),  # noqa

            (TESTDATA.case7_using_file_scenario1.fmt % (text_output_filename, template_filename), TESTDATA.case7_using_file_scenario1.expected_result),  # noqa
            (TESTDATA.case7_using_file_scenario2.fmt % (text_output_filename, template_filename), TESTDATA.case7_using_file_scenario2.expected_result),  # noqa
        ]
    )
    def test_or_verify(self, cmdline, expected_result):
        result = MiscOutput.execute_shell_command(cmdline)
        reformat_result = ReformatOutput(result.output)
        assert result.is_success
        assert reformat_result.strip() == expected_result
