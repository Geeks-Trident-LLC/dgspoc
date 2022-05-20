
from pathlib import Path

import pytest

from dgspoc.utils import MiscOutput

from . import get_tmp_file_path

file1 = get_tmp_file_path()
file2 = get_tmp_file_path()
folder1 = get_tmp_file_path(is_folder=True)
folder2 = get_tmp_file_path(is_folder=True)


class TestConsoleDeleteFlag:

    def setup_method(self):     # noqa
        for fn in [file1, file2]:
            node = Path(fn)
            not node.exists() and node.touch()
            assert node.is_file()

        for folder in [folder1, folder2]:
            node = Path(folder)
            not node.exists() and node.mkdir()
            assert node.is_dir()

    @pytest.mark.parametrize(
        'cmdline',
        [
            'dgs --delete="%s"' % file1,
            'dgs --delete="%s %s"' % (file1, file2),
            'dgs --delete="%s, %s"' % (file1, file2),
            'dgs --delete="%s  ,  %s"' % (file1, file2),
            'dgs --delete="{%s,  %s}"' % (file1, file2),
            'dgs --delete="%s"' % folder1,
            'dgs --delete="%s %s"' % (file1, folder1),
            'dgs --delete="%s, %s, %s, %s"' % (file1, file2, folder1, folder2),
        ]
    )
    def test_console_delete_flag(self, cmdline):
        result = MiscOutput.execute_shell_command(cmdline)
        assert result.is_success

        for line in result.output.splitlines():
            if line.strip():
                assert 'Successfully deleted ' in line

