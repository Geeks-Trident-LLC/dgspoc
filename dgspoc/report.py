"""Module containing the logic for report of test execution"""

import re
from os import path
from glob import glob

from datetime import datetime

from dgspoc.constant import FWTYPE
from dgspoc.exceptions import ReportError

from xml.etree import ElementTree


class DGSReport:
    def __init__(self, *report_files, detail=False):
        if not report_files:
            raise ReportError('CANT generate report without report file.')

        self.report_files = report_files
        self.detail = detail

    def generate(self):
        lst = []
        for report_file in self.report_files:
            if 'unittest' in report_file:
                report_content = self.generate_unittest_report(report_file)
            elif 'pytest' in report_file:
                report_content = self.generate_pytest_report(report_file)
            else:
                report_content = self.generate_robotframework_report(report_file)

            if report_content.strip():
                lst and lst.append('')
                lst.append(report_content)

        all_reports = '\n'.join(lst)
        return all_reports

    def generate_unittest_report(self, file_name):
        tree = ElementTree.parse(file_name)
        root = tree.getroot()
        return ''

    def generate_pytest_report(self, file_name):
        tree = ElementTree.parse(file_name)
        root = tree.getroot()
        return ''

    def generate_robotframework_report(self, file_name):
        tree = ElementTree.parse(file_name)
        root = tree.getroot()

        suite_node = root.find('suite')
        statistics_node = root.find('statistics')
        errors_node = root.find('errors')

        lst = ['Robotframework Report', '-' * 21]

        return ''

    @classmethod
    def generate_report(cls, directory=''):
        report_files = DGSReportFile.get_report_files(directory=directory)
        report = cls(*report_files)

        report_content = report.generate()
        return report_content

    
class DGSReportFile:
    def __init__(self, filename):
        self.filename = str(filename).strip()
        self.basename = path.basename(self.filename)
    
    @property
    def is_report_file(self):
        chk = self.is_unittest
        chk &= self.is_pytest
        chk &= self.is_robotframework
        return chk
    
    @property
    def is_unittest(self):
        chk = self.check_report_file(FWTYPE.UNITTEST)
        return chk
    
    @property
    def is_pytest(self):
        chk = self.check_report_file(FWTYPE.PYTEST)
        return chk
    
    @property
    def is_robotframework(self):
        chk = self.check_report_file(FWTYPE.ROBOTFRAMEWORK)
        return chk
    
    def get_prefix(self, framework):    # noqa
        other = 'output' if framework == FWTYPE.ROBOTFRAMEWORK else 'report'
        prefix = '%s_%s' % (framework, other)
        return prefix

    def check_report_file(self, framework):
        prefix = self.get_prefix(framework)
        fmt = '%s_[0-9]{4}[a-z]{3}[0-9]{2}_[0-9]{6}[.]xml'
        pattern = fmt % prefix
        match = re.match(pattern, self.basename)
        return bool(match)

    @classmethod
    def get_report_files(cls, directory=''):

        report_files = []
        lookups = ['unittest_report_*_*.xml',
                   'pytest_report_*_*.xml',
                   'robotframework_output_*_*.xml']
        for lookup in lookups:
            report_file = cls.get_report_file_by(lookup, directory=directory)
            report_file and report_files.append(report_file)

        return report_files

    @classmethod
    def get_report_file_by(cls, lookup, directory=''):
        directory = directory.strip()
        file_path = path.join(directory, lookup)
        lst = glob(file_path)
        if not lst:
            return ''

        base_dt = datetime(1900, 1, 1)
        fmt1 = 'unittest_report_%Y%b%d_%H%M%S.xml'
        fmt2 = 'pytest_report_%Y%b%d_%H%M%S.xml'
        fmt3 = 'robotframework_output_%Y%b%d_%H%M%S.xml'
        report_file = ''

        for file_name in lst:
            file_obj = cls(file_name)
            if file_obj.is_unittest:
                pass
            elif file_obj.is_pytest:
                pass
            elif file_obj.is_robotframework:
                pass

            if file_name.startswith('unittest_report_'):
                fmt = fmt1
            else:
                fmt = fmt2 if file_name.startswith('pytest_report_') else fmt3
            dt = datetime.strptime(file_name, fmt)
            if dt > base_dt:
                report_file = file_name
                base_dt = dt
        return report_file
