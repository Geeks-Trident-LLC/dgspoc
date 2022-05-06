from subprocess import getstatusoutput

import pytest

from dgspoc.constant import ECODE
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
    """Note: comment line will be work as same as previous"""
    @pytest.mark.parametrize(
        'cmdline',
        [
            'dgs build template --help',
            # 'dgs build template usage',
        ]
    )
    def test_build_template_help(self, cmdline):
        exit_code, output = getstatusoutput(cmdline)

        assert exit_code == ECODE.SUCCESS
        assert 'dgs build template usage' in output
        assert ' --author AUTHOR ' in output
        assert ' --email EMAIL ' in output
        assert ' --company COMPANY ' in output
        assert ' --save-to FILENAME ' in output
        assert ' --template-id TMPLID ' in output
        assert ' --replaced ' in output
        assert ' -h, --help ' in output
        assert 'dgs build template operands [options]' in output
        assert 'dgs build template example ' in output

    @pytest.mark.parametrize(
        ('cmdline', 'expected_result'),
        [
            (base_cmdline, TESTDATA.expected_result_wo_user_info),
            (cmdline_with_user_info, TESTDATA.expected_result_with_user_info),
        ]
    )
    def test_build_template(self, cmdline, expected_result):
        exit_code, output = getstatusoutput(cmdline)
        template_txt = MiscOutput.clean_created_date_stamp(output)
        template_txt.strip()

        assert exit_code == ECODE.SUCCESS
        assert template_txt == expected_result

    @pytest.mark.parametrize(
        'cmdline',
        [
            '%s --template-id=%s --replace' % (cmdline_with_user_info,
                                               TESTDATA.template_id)
        ]
    )
    def test_build_template_and_save_to_storage(self, cmdline):
        exit_code, _skip = getstatusoutput(cmdline)
        assert exit_code == ECODE.SUCCESS
