import re

import pytest

from dgspoc.constant import ECODE
from dgspoc.main import Cli
from dgspoc.utils import MiscOutput


class TestConsoleHelpFlag:
    def setup_class(self):
        result = MiscOutput.execute_shell_command('dgs --help')
        self.exit_code = result.exit_code
        self.output = result.output

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
    """Note: the comment in pytest.mark.parametrize should work as same as
    the previous command line"""

    @pytest.mark.parametrize(
        'cmdline',
        [
            'dgs --version',
            # 'dgs -v',
            # 'dgs version',
        ]
    )
    def test_version_flag(self, cmdline):
        result = MiscOutput.execute_shell_command(cmdline)

        assert result.is_success

        pattern = r'(?i)%s +v[0-9]+([.][0-9]+)*' % Cli.prog
        match = re.match(pattern, result.output)
        chk = bool(match)
        assert chk is True


class TestConsoleInfoCommand:
    """Note: the comment in pytest.mark.parametrize should work as same as
    the previous command line"""

    def test_info_help_flag(self):
        cmdline = 'dgs info --help'
        result = MiscOutput.execute_shell_command(cmdline)
        assert result.is_success
        assert 'dgs info usage' in result.output
        assert ' --all          ' in result.output
        assert ' --dependency   ' in result.output
        assert ' --template-storage  ' in result.output
        assert ' -h, --help ' in result.output
        assert 'dgs info operands [options]' in result.output
        assert 'dgs info example ' in result.output

    def test_info_command(self):
        cmdline = 'dgs info'
        result = MiscOutput.execute_shell_command(cmdline)

        assert result.is_success
        assert Cli.prog_fn.title() in result.output
        assert '| Project : ' in result.output
        assert '| License : ' in result.output
        assert '| Platform: ' in result.output

    @pytest.mark.parametrize(
        'cmdline',
        [
            'dgs info --dependency',
            # 'dgs info dependency',
            # 'dgs info depend',
        ]
    )
    def test_info_dependency_command(self, cmdline):
        result = MiscOutput.execute_shell_command(cmdline)

        assert result.is_success
        assert ' Package: compare_versions ' in result.output
        assert ' Package: dlapp ' in result.output
        assert ' Package: pytest ' in result.output
        assert ' Package: python-dateutil ' in result.output
        assert ' Package: pyyaml ' in result.output
        assert ' Package: regexapp ' in result.output
        assert ' Package: robotframework ' in result.output
        assert ' Package: templateapp ' in result.output
        assert ' Package: textfsm ' in result.output

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
        result = MiscOutput.execute_shell_command(cmdline)

        assert result.is_success
        assert ' Template Storage Info: ' in result.output
        assert '   - Location: ' in result.output
        assert '   - Existed: ' in result.output
        assert '   - Total Templates: ' in result.output

    @pytest.mark.parametrize(
        'cmdline',
        [
            'dgs info --all',
            # 'dgs info all',
        ]
    )
    def test_info_dependency_command(self, cmdline):
        result = MiscOutput.execute_shell_command(cmdline)

        assert result.is_success

        assert Cli.prog_fn.title() in result.output
        assert '| Project : ' in result.output
        assert '| License : ' in result.output
        assert '| Platform: ' in result.output

        assert ' Package: compare_versions ' in result.output
        assert ' Package: dlapp ' in result.output
        assert ' Package: pytest ' in result.output
        assert ' Package: python-dateutil ' in result.output
        assert ' Package: pyyaml ' in result.output
        assert ' Package: regexapp ' in result.output
        assert ' Package: robotframework ' in result.output
        assert ' Package: templateapp ' in result.output
        assert ' Package: textfsm ' in result.output

        assert ' Template Storage Info: ' in result.output
        assert '   - Location: ' in result.output
        assert '   - Existed: ' in result.output
        assert '   - Total Templates: ' in result.output
