import pytest

from dgspoc.utils import File
from dgspoc.utils import MiscOutput

from . import ReformatOutput

TESTDATA = File.get_result_from_yaml_file(
    'data/console_build_batch_cli_data.yaml',
    base_dir=__file__,
    dot_datatype=True,
    var_substitution=True,
    root_var_name='self'
)


class TestConsoleBuildBatchCommandLineUsage:
    """Note: the comment in pytest.mark.parametrize should work as same as
    the previous command line"""

    @pytest.mark.parametrize(
        'cmdline',
        [
            'dgs build batch --help',
        ]
    )
    def test_console_cli_help(self, cmdline):
        result = MiscOutput.execute_shell_command(cmdline)

        assert result.is_success
        assert 'dgs build batch usage' in result.output
        assert ' --save-to FILENAME ' in result.output
        assert ' -h, --help ' in result.output
        assert 'dgs build batch operands [options]' in result.output
        assert 'dgs build batch example ' in result.output


class TestConsoleBuildBatchScript:
    def setup_method(self):     # noqa
        File.save(TESTDATA.scripts.unittest.filename, TESTDATA.scripts.unittest.content)
        File.save(TESTDATA.scripts.pytest.filename, TESTDATA.scripts.pytest.content)
        File.save(TESTDATA.scripts.robotframework.filename, TESTDATA.scripts.robotframework.content)

    def teardown_method(self):  # noqa
        File.delete(TESTDATA.scripts.src_dir)
        File.delete(TESTDATA.scripts.dst_dir)

    @pytest.mark.parametrize(
        ('cmdline', 'expected_result'),
        [
            (TESTDATA.case1.cmdline, TESTDATA.case1.expected_result),   # noqa
            (TESTDATA.case2.cmdline, TESTDATA.case2.expected_result),   # noqa
            (TESTDATA.case3.cmdline, TESTDATA.case3.expected_result),   # noqa
            (TESTDATA.case4.cmdline, TESTDATA.case4.expected_result),   # noqa
        ]
    )
    def test_building_batch_script(self, cmdline, expected_result):
        result = MiscOutput.execute_shell_command(cmdline)
        reformat_result = ReformatOutput(result.output, everything=True)
        assert result.is_success
        assert reformat_result.strip() == expected_result

    @pytest.mark.parametrize(
        ('cmdline', 'batch_filename'),
        [
            (TESTDATA.case5.cmdline, TESTDATA.case5.batch_filename),   # noqa
        ]
    )
    def test_building_batch_script_and_save_to_file(self, cmdline, batch_filename):
        result = MiscOutput.execute_shell_command(cmdline)
        reformat_result = ReformatOutput(result.output, everything=True)
        assert result.is_success
        assert '+++ Successfully saved ' in result.output
        File.delete(batch_filename)
