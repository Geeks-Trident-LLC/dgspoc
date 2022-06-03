import pytest

from dgspoc.utils import File
from dgspoc.utils import MiscOutput
from dgspoc.constant import FWTYPE

from os import path
from tempfile import gettempdir
from time import time

from . import ReformatOutput

TESTDATA = File.get_result_from_yaml_file(
    'data/console_build_script_cli_data.yaml',
    base_dir=__file__,
    dot_datatype=True,
    var_substitution=True,
    root_var_name='self'
)

base_dir = File.get_dir(__file__)
snippet_filename = File.get_path(base_dir, 'data/snippet_for_script_builder.txt')


def get_temp_file(framework):
    extension = 'robot' if framework == FWTYPE.ROBOTFRAMEWORK else 'py'
    base_file = 'test_generated_script_%d.%s' % (time(), extension)
    tmp_file = path.join(gettempdir(), base_file)
    return tmp_file


class TestConsoleBuildScriptCommandLineUsage:
    """Note: the comment in pytest.mark.parametrize should work as same as
    the previous command line"""

    @pytest.mark.parametrize(
        'cmdline',
        [
            'dgs build unittest --help',
            # 'dgs build unittest_script --help',
            # 'dgs build pytest --help',
            # 'dgs build pytest_script --help',
            # 'dgs build robotframework --help',
            # 'dgs build robotframework_script --help',
        ]
    )
    def test_console_cli_help(self, cmdline):
        result = MiscOutput.execute_shell_command(cmdline)

        assert result.is_success
        assert 'dgs build script usage' in result.output
        assert ' --author AUTHOR ' in result.output
        assert ' --email EMAIL ' in result.output
        assert ' --company COMPANY ' in result.output
        assert ' --save-to FILENAME ' in result.output
        assert ' -h, --help ' in result.output
        assert 'dgs build script operands [options]' in result.output
        assert 'dgs build script example ' in result.output


class TestConsoleBuildTestScript:
    @pytest.mark.parametrize(
        ('cmdline', 'expected_result'),
        [
            (TESTDATA.unittest.fmt % snippet_filename, TESTDATA.unittest.expected_result),              # noqa
            (TESTDATA.pytest.fmt % snippet_filename, TESTDATA.pytest.expected_result),                  # noqa
            (TESTDATA.robotframework.fmt % snippet_filename, TESTDATA.robotframework.expected_result),  # noqa
        ]
    )
    def test_building_test_script(self, cmdline, expected_result):
        result = MiscOutput.execute_shell_command(cmdline)
        reformat_result = ReformatOutput(result.output, everything=True)
        assert result.is_success
        assert reformat_result.strip() == expected_result

    @pytest.mark.parametrize(
        'cmdline',
        [
            TESTDATA.fmt_with_save_to % ('unittest', snippet_filename, get_temp_file('unittest')),              # noqa
            TESTDATA.fmt_with_save_to % ('pytest', snippet_filename, get_temp_file('pytest')),                  # noqa
            TESTDATA.fmt_with_save_to % ('robotframework', snippet_filename, get_temp_file('robotframework')),  # noqa
        ]
    )
    def test_building_test_script_and_save_to_file(self, cmdline):
        result = MiscOutput.execute_shell_command(cmdline)
        assert result.is_success
        assert 'Successfully saved the generated test script to' in result.output
