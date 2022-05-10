import pytest
from tempfile import gettempdir
from time import time
from os import path

from dgspoc.utils import File
from dgspoc.utils import MiscOutput

from . import ReformatOutput

TESTDATA = File.get_result_from_yaml_file(
    'data/console_build_template_cli_data.yaml',
    base_dir=__file__,
    dot_datatype=True,
    var_substitution=True,
    root_var_name='self'
)

tmp_file = path.join(gettempdir(), 'test_file_%d.txt' % time())


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
            (TESTDATA.built_tmpl_cmdline, TESTDATA.expected_result_wo_user_info),
            (TESTDATA.built_tmpl_with_user_info_cmdline, TESTDATA.expected_result_with_user_info),
        ]
    )
    def test_build_template(self, cmdline, expected_result):
        result = MiscOutput.execute_shell_command(cmdline)
        template_txt = str(ReformatOutput(result.output))
        template_txt.strip()
        assert result.is_success
        assert template_txt == expected_result


class TestBuildTemplateAndSaveToTemplateStorage:

    def setup_class(self):      # noqa
        MiscOutput.execute_shell_command(TESTDATA.cleared_tmpl_in_storage_cmdline)

    def teardown_class(self):   # noqa
        MiscOutput.execute_shell_command(TESTDATA.cleared_tmpl_in_storage_cmdline)

    @pytest.mark.parametrize(
        'cmdline',
        [
            TESTDATA.built_tmpl_and_saved_to_storage_cmdline,
            TESTDATA.built_tmpl_and_replaced_in_storage_cmdline,
        ]
    )
    def test_build_template_and_save_to_template_storage(self, cmdline):
        result = MiscOutput.execute_shell_command(cmdline)
        assert result.is_success
        assert 'Successfully uploaded ' in result.output
        assert '"%s" template ID' % TESTDATA.template_id in result.output


class TestBuildTemplateAndSaveToFile:
    @pytest.mark.parametrize(
        'cmdline',
        [
            '%s --save-to="%s"' % (TESTDATA.built_tmpl_cmdline, tmp_file),
        ]
    )
    def test_build_template_and_save_to_file(self, cmdline):
        result = MiscOutput.execute_shell_command(cmdline)
        MiscOutput.execute_shell_command('dgs --clear="--filename=%s"' % tmp_file)
        assert result.is_success
        assert 'Successfully saved generated template ' in result.output
