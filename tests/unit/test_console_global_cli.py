import re
from subprocess import getstatusoutput

import pytest

from dgspoc.constant import ECODE
from dgspoc.main import Cli


class TestConsoleHelpFlag:
    def setup_class(self):
        self.exit_code, self.output = getstatusoutput('dgs --help')

    def test_exit_code(self):
        assert self.exit_code == ECODE.SUCCESS

    @pytest.mark.parametrize(
        'expected_result',
        [
            sorted(['build', 'info', 'run', 'search',
                    'test', 'version', 'usage'])
        ]
    )
    def test_position_command_flag(self, expected_result):
        lines = self.output.splitlines()
        pattern = r'(?i) +command + command +must +be +either +(?P<data>\w.*\S) *$'

        commands = []

        for index, line in enumerate(lines):
            match = re.match(pattern, line)
            if match:
                next_line = ''.join(lines[index + 1:index + 2])
                next_line = next_line.strip() if next_line.startswith(' ' * 12) else ''

                data = '%s %s' % (match.group('data'), next_line)
                data = data.replace(' or', '')
                commands = sorted(re.split(r' *, *', data))
                assert commands == expected_result
                return

        assert commands == expected_result

    @pytest.mark.parametrize(
        'positional_argument',
        [
            ' -h, --help ',
            ' -v, --version ',
            ' --author AUTHOR ',
            ' --email EMAIL ',
            ' --company COMPANY ',
            ' --save-to FILENAME ',
            ' --template-id TMPLID ',
            ' --adaptor ADAPTOR ',
            ' --action ACTION ',
            ' --replaced ',
            ' --dependency ',
            ' --template-storage '
        ]
    )
    def test_position_command_flag(self, positional_argument):
        chk = positional_argument in self.output
        assert chk is True


class TestConsoleVersionCommand:
    """Note: comment line will be work as same as previous"""
    @pytest.mark.parametrize(
        'cmdline',
        [
            'dgs --version',
            # 'dgs -v',
            # 'dgs version',
        ]
    )
    def test_version_flag(self, cmdline):
        exit_code, output = getstatusoutput(cmdline)

        assert exit_code == ECODE.SUCCESS

        pattern = r'(?i)%s +v[0-9]+([.][0-9]+)*' % Cli.prog
        match = re.match(pattern, output)
        chk = bool(match)
        assert chk is True


class TestConsoleInfoCommand:
    """Note: comment line will be work as same as previous"""

    def test_info_help_flag(self):
        cmdline = 'dgs info --help'
        exit_code, output = getstatusoutput(cmdline)
        assert exit_code == ECODE.SUCCESS
        assert 'dgs info usage' in output
        assert ' --all          ' in output
        assert ' --dependency   ' in output
        assert ' --template-storage  ' in output
        assert ' -h, --help ' in output
        assert 'dgs info operands [options]' in output
        assert 'dgs info example ' in output

    def test_info_command(self):
        cmdline = 'dgs info'
        exit_code, output = getstatusoutput(cmdline)

        assert exit_code == ECODE.SUCCESS
        assert Cli.prog_fn.title() in output
        assert '| Project : ' in output
        assert '| License : ' in output
        assert '| Platform: ' in output

    @pytest.mark.parametrize(
        'cmdline',
        [
            'dgs info --dependency',
            # 'dgs info dependency',
            # 'dgs info depend',
        ]
    )
    def test_info_dependency_command(self, cmdline):
        exit_code, output = getstatusoutput(cmdline)

        assert exit_code == ECODE.SUCCESS
        assert ' Package: compare_versions ' in output
        assert ' Package: dlapp ' in output
        assert ' Package: pytest ' in output
        assert ' Package: python-dateutil ' in output
        assert ' Package: pyyaml ' in output
        assert ' Package: regexapp ' in output
        assert ' Package: robotframework ' in output
        assert ' Package: templateapp ' in output
        assert ' Package: textfsm ' in output

    @pytest.mark.parametrize(
        'cmdline',
        [
            'dgs info --template-storage',
            # 'dgs info template-storage',
            # 'dgs info template',
            # 'dgs info storage',
        ]
    )
    def test_info_dependency_command(self, cmdline):
        exit_code, output = getstatusoutput(cmdline)

        assert exit_code == ECODE.SUCCESS
        assert ' Template Storage Info: ' in output
        assert '   - Location: ' in output
        assert '   - Existed: ' in output
        assert '   - Total Templates: ' in output

    @pytest.mark.parametrize(
        'cmdline',
        [
            'dgs info --all',
            # 'dgs info all',
        ]
    )
    def test_info_dependency_command(self, cmdline):
        exit_code, output = getstatusoutput(cmdline)

        assert exit_code == ECODE.SUCCESS

        assert Cli.prog_fn.title() in output
        assert '| Project : ' in output
        assert '| License : ' in output
        assert '| Platform: ' in output

        assert ' Package: compare_versions ' in output
        assert ' Package: dlapp ' in output
        assert ' Package: pytest ' in output
        assert ' Package: python-dateutil ' in output
        assert ' Package: pyyaml ' in output
        assert ' Package: regexapp ' in output
        assert ' Package: robotframework ' in output
        assert ' Package: templateapp ' in output
        assert ' Package: textfsm ' in output

        assert ' Template Storage Info: ' in output
        assert '   - Location: ' in output
        assert '   - Existed: ' in output
        assert '   - Total Templates: ' in output
