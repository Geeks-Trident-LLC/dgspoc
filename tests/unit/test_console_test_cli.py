import pytest

from dgspoc.utils import File
from dgspoc.utils import MiscOutput

TESTDATA = File.get_result_from_yaml_file(
    'data/console_build_template_cli_data.yaml',
    base_dir=__file__,
    dot_datatype=True
)

base_cmdline = 'dgs build template "%s"' % TESTDATA.user_data
fmt = '--author="%(author)s" --email="%(email)s" --company="%(company)s"'
postfix = fmt % TESTDATA.user_info
cmdline_with_user_info = '%s %s' % (base_cmdline, postfix)


class TestBuildTemplate:
    """Note: the comment in pytest.mark.parametrize should work as same as
    the previous command line"""

    @pytest.mark.parametrize(
        'cmdline',
        [
            'dgs build template --help',
            # 'dgs build template usage',
        ]
    )
    def test_build_template_help(self, cmdline):
        result = MiscOutput.execute_shell_command(cmdline)

        assert result.is_success
        assert 'dgs build template usage' in result.output
        assert ' --author AUTHOR ' in result.output
        assert ' --email EMAIL ' in result.output
        assert ' --company COMPANY ' in result.output
        assert ' --save-to FILENAME ' in result.output
        assert ' --template-id TMPLID ' in result.output
        assert ' --replaced ' in result.output
        assert ' -h, --help ' in result.output
        assert 'dgs build template operands [options]' in result.output
        assert 'dgs build template example ' in result.output

    @pytest.mark.parametrize(
        ('cmdline', 'expected_result'),
        [
            (base_cmdline, TESTDATA.expected_result_wo_user_info),
            (cmdline_with_user_info, TESTDATA.expected_result_with_user_info),
        ]
    )
    def test_build_template(self, cmdline, expected_result):
        result = MiscOutput.execute_shell_command(cmdline)
        template_txt = MiscOutput.clean_created_date_stamp(result.output)
        template_txt.strip()

        assert result.is_success
        assert template_txt == expected_result

    @pytest.mark.parametrize(
        'cmdline',
        [
            '%s --template-id=%s --replace' % (cmdline_with_user_info,
                                               TESTDATA.template_id)
        ]
    )
    def test_build_template_and_save_to_storage(self, cmdline):
        result = MiscOutput.execute_shell_command(cmdline)
        assert result.is_success
