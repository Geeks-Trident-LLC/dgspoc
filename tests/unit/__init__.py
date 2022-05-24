import re
import sys
import time
from os import path

from pathlib import Path
from tempfile import gettempdir


def check_python_version(major=-1, minor=-1, micro=-1):
    if major == minor and major == micro and major == -1:
        return False

    lst = [
        (major, sys.version_info.major),
        (minor, sys.version_info.minor),
        (micro, sys.version_info.micro)
    ]
    chk = True
    for val, expected_val in lst:
        if val >= 0:
            chk &= val == expected_val
    return chk


def is_py36_or_py37():
    chk1 = check_python_version(major=3, minor=6)
    chk2 = check_python_version(major=3, minor=7)
    chk = chk1 or chk2
    return chk


def get_tmp_dir():
    tmp_dir = gettempdir()
    return tmp_dir


def get_tmp_file_path(prefix='', is_folder=False, extension='txt'):
    time.sleep(0.012345)
    tmp_dir = gettempdir()
    stamp = str(time.time()).replace('.', '_')
    if is_folder:
        fmt = '%s_%%s' % (prefix or 'tmp_folder')
        file_path = str(Path(tmp_dir, fmt % stamp))
        return file_path

    if extension:
        fmt = '%s_%%s.%%s' % (prefix or 'tmp_file')
        file_path = str(Path(tmp_dir, fmt % (stamp, extension.lstrip('.'))))
        return file_path
    else:
        fmt = '%s_%%s' % (prefix or 'tmp_file')
        file_path = str(Path(tmp_dir, fmt % stamp))
        return file_path


def get_test_data_file(filename):
    base_dir = path.dirname(__file__)
    fullpath = path.join(base_dir, 'data', filename)
    return fullpath


class ReformatOutput:
    def __init__(self, raw_data, everything=False):
        self.device_name = ''
        self.raw_data = str(raw_data)
        self.everything = everything
        self.output = ''
        self.process()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            chk = self.output == other.output
            return chk
        elif isinstance(other, str):
            new_other = other.replace('{device_name}', self.device_name)
            chk = self.output == new_other
            return chk
        return False

    def __repr__(self):
        return self.output

    def __str__(self):
        return self.output

    def strip(self, characters=''):
        if characters:
            self.output = self.output.strip(characters)
        else:
            self.output = self.output.strip()
        return self

    def process(self):
        if self.raw_data.strip() == '':
            return

        lines = self.raw_data.splitlines()
        lst = []
        excluded_txt_pat = r'^ERROR: .+? [<>=]{1,2} .+?$'
        service_stamp_pat = r'(?i)- UNREAL-DEVICE-[a-z]+-SERVICE-TIMESTAMP'
        replacing_service_stamp_pat = r'(?i)^[a-z]{3} \d{2} \d{4} \d{2}:\d{2}:\d{2}[.]\d{3}'
        replacing_created_date_pat = r'(?i)^(# Created date:) (\d{4}-\d\d-\d\d)( *)$'

        pat = (r'(?i)=(unittest|pytest|robotframework)_(report|output|log)_'
               r'([0-9]{4}[a-z]{3}[0-9]{2}_[0-9]{6})[.](xml|html)')
        replacing_report_filename_pat = pat

        report_pat = (r'(?i)(unittest|pytest|robotframework) (report - \w+) '
                      r'([0-9.]+) (- Python) ([0-9.]+) on (\w+)')

        device_name_pat = r'(?i)(?P<name>\S+) +is +(successfully +)?((dis)?connected)[.]'
        for index, line in enumerate(lines):
            if re.match(excluded_txt_pat, line):
                continue
            elif self.everything and re.search(service_stamp_pat, line):
                changed_txt = re.sub(replacing_service_stamp_pat,
                                     'mmm dd yyyy HH:MM:SS.###', line)
                lst.append(changed_txt)
            elif self.everything and re.match(replacing_created_date_pat, line):
                changed_txt = re.sub(replacing_created_date_pat,
                                     r'\1 yyyy-mm-dd\3', line)
                lst.append(changed_txt)
            elif self.everything and re.search(replacing_report_filename_pat, line):
                changed_txt = re.sub(replacing_report_filename_pat,
                                     r'=\1_\2_yyyymmmdd_HHMMSS.\4', line)
                lst.append(changed_txt)
            elif self.everything and re.match(report_pat, line.strip('| ')):
                line = line.strip('| ')
                changed_txt = re.sub(report_pat, r'\1 \2 #.#.# \4 #.#.# on O.S', line)
                lst.append('| %s |' % changed_txt.ljust(76))
                next_changed_txt = '-' * len(changed_txt)
                lines[index + 1] = '| %s |' % next_changed_txt.ljust(76)
            else:
                lst.append(line)
                match = re.match(device_name_pat, line)
                if match and not self.device_name:
                    self.device_name = match.group('name')

        self.output = '\n'.join(lst)
