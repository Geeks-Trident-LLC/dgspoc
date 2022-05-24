import pytest
import platform

from dgspoc.utils import File
from dgspoc.utils import MiscOutput

from dgspoc.report import DGSReportFile

from . import ReformatOutput

TESTDATA = File.get_result_from_yaml_file(
    'data/console_report_cli_data.yaml',
    base_dir=__file__,
    dot_datatype=True,
    var_substitution=True,
    root_var_name='self'
)

is_window = platform.system().lower() == 'windows'
batch_cmdline = TESTDATA.dos_cmdline if is_window else TESTDATA.shell_cmdline


class TestConsoleReportCommandLineUsage:
    """Note: the comment in pytest.mark.parametrize should work as same as
    the previous command line"""

    @pytest.mark.parametrize(
        'cmdline',
        [
            'dgs report --help',
        ]
    )
    def test_console_cli_help(self, cmdline):
        result = MiscOutput.execute_shell_command(cmdline)

        assert result.is_success
        assert 'dgs report usage' in result.output
        assert ' --detail ' in result.output
        assert ' -h, --help ' in result.output
        assert 'dgs report operands [options]' in result.output
        assert 'dgs report example ' in result.output


class TestConsoleBuildBatchScript:
    def setup_method(self):     # noqa
        File.save(TESTDATA.snippet_file, TESTDATA.snippet_content)

    def teardown_method(self):  # noqa
        File.delete(TESTDATA.user_folder)
        File.delete(TESTDATA.batch_file)
        report_files = DGSReportFile.get_report_files()

        for report_file in report_files:
            File.delete(report_file)
            if 'robotframework_output' in report_file:
                log_file = report_file.replace('_output_', '_log_')
                log_file = log_file.replace('.xml', '.html')
                File.delete(log_file)
                other_file = report_file.replace('_output_', '_report_')
                other_file = other_file.replace('.xml', '.html')
                File.delete(other_file)

    @pytest.mark.parametrize(
        ('cmdlines', 'expected_result'),
        [
            (TESTDATA.case1.fmt % batch_cmdline, TESTDATA.case1.expected_result),   # noqa
            (TESTDATA.case2.fmt % batch_cmdline, TESTDATA.case2.expected_result),  # noqa
            (TESTDATA.case3.fmt % batch_cmdline, TESTDATA.case3.expected_result),  # noqa
            (TESTDATA.case4.fmt % batch_cmdline, TESTDATA.case4.expected_result),  # noqa
            (TESTDATA.case5.fmt % batch_cmdline, TESTDATA.case5.expected_result),  # noqa
            (TESTDATA.case6.fmt % batch_cmdline, TESTDATA.case6.expected_result),  # noqa
        ]
    )
    def test_building_batch_script(self, cmdlines, expected_result):

        reformat_result = None

        for cmdline in cmdlines.splitlines():
            result = MiscOutput.execute_shell_command(cmdline)
            reformat_result = ReformatOutput(result.output, everything=True)
            assert result.is_success
        else:
            if reformat_result:
                assert expected_result in str(reformat_result)
