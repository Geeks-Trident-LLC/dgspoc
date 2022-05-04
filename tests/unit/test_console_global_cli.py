import re
from subprocess import getstatusoutput

import pytest

from dgspoc.constant import ECODE
from dgspoc.main import Cli


class TestConsoleHelpFlag:
    exit_code, output = getstatusoutput('dgs --help')

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
        'positional_arguments',
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
    def test_position_command_flag(self, positional_arguments):
        chk = positional_arguments in self.output
        assert chk is True


class TestConsoleVersionCommand:
    """Note: comment line will be work as same as previous"""
    @pytest.mark.parametrize(
        'cmdline',
        [
            'dgs --version',
            # 'dgs version',      # this command works the same above
        ]
    )
    def test_version_flag(self, cmdline):
        exit_code, output = getstatusoutput(cmdline)

        assert exit_code == ECODE.SUCCESS

        pattern = r'(?i)%s +v[0-9]+([.][0-9]+)*' % Cli.prog
        match = re.match(pattern, output)
        chk = bool(match)
        assert chk is True
