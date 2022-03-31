"""Module containing the logic for describe-get-system proof of conception entry-points."""

import sys
import argparse

from dgspoc import version
from dgspoc.config import Data

from dgspoc.utils import Printer
from dgspoc.utils import ECODE

from dgspoc.usage import validate_usage
from dgspoc.usage import show_usage

from dgspoc.operation import do_build_template
from dgspoc.operation import do_search_template
from dgspoc.operation import do_test_template


def show_info(options):
    command, operands = options.command, options.operands
    if command == 'info':
        validate_usage(command, operands)

        if len(operands) > 1:
            show_usage(command, exit_code=ECODE.BAD)

        lst = ['Describe-Get-System Proof of Concept', Data.get_app_info()]

        info_type = operands[0].lower() if operands else ''
        if info_type and info_type in ['all', 'dependency']:
            lst.append('--------------------')
            lst.append('Dependencies:')
            for pkg in Data.get_dependency().values():
                lst.append('  + Package: {0[package]}'.format(pkg))
                lst.append('             {0[url]}'.format(pkg))

        if info_type and info_type in ['all', 'template']:
            lst.append('--------------------',)
            lst.append(Data.get_template_storage_info())

        Printer.print(lst)
        sys.exit(ECODE.SUCCESS)


def show_version(options):
    if options.command == 'version':
        print('{} v{}'.format(Cli.prog, version))
        sys.exit(ECODE.SUCCESS)


class Cli:
    """describe-get-system proof of concept console CLI application."""
    prog = 'dgs'
    prog_fn = 'describe-get-system'
    commands = ['build', 'info', 'run', 'search', 'test', 'version']

    def __init__(self):
        parser = argparse.ArgumentParser(
            prog=self.prog,
            usage='%(prog)s [options] command operands',
            description='{} proof of concept'.format(self.prog_fn),
        )

        parser.add_argument(
            '-v', '--version', action='version',
            version='%(prog)s v{}'.format(version)
        )

        parser.add_argument(
            '--author', type=str, default='',
            help="author's name"
        ),

        parser.add_argument(
            '--email', type=str, default='',
            help="author's email"
        ),

        parser.add_argument(
            '--company', type=str, default='',
            help="author's company"
        ),

        parser.add_argument(
            '--save', type=str, dest='filename', default='',
            help="saving to file"
        ),

        parser.add_argument(
            '--template-id', type=str, dest='tmplid', default='',
            help="template ID"
        ),

        parser.add_argument(
            '--test-file', type=str, dest='testfile', default='',
            help="test data file"
        ),

        parser.add_argument(
            '--adaptor', type=str, default='',
            help="connector adaptor"
        ),

        parser.add_argument(
            '--execution', type=str, default='',
            help="command line"
        ),

        parser.add_argument(
            '--replaced', action='store_true',
            help='overwrite template ID/file'
        )

        parser.add_argument(
            '--ignore-case', action='store_true', dest='ignore_case',
            help='case insensitive matching'
        )

        parser.add_argument(
            '--showed', action='store_true',
            help='showing result'
        )

        parser.add_argument(
            '--tabular', action='store_true',
            help='showing result in tabular format'
        )

        parser.add_argument(
            'command', type=str,
            help='command must be either build, '
                 'info, run, search, test, or version'
        )
        parser.add_argument(
            'operands', nargs='*', type=str,
            help='operands can be template, unittest, '
                 'pytest, robotframework, script, or data such command-line, '
                 'config-lines, or filename'
        )

        self.kwargs = dict()
        self.parser = parser
        try:
            self.options = self.parser.parse_args()
        except SystemExit as ex:     # noqa
            self.parser.print_help()
            sys.exit(ECODE.BAD)

    def validate_command(self):
        """Validate argparse `options.command`.

        Returns
        -------
        bool: show ``self.parser.print_help()`` and call ``sys.exit(ECODE.BAD)`` if
        command is neither build, info, run, search,
        test, nor version, otherwise, return True
        """
        self.options.command = self.options.command.lower()

        if self.options.command in self.commands:
            return True
        self.parser.print_help()
        sys.exit(ECODE.BAD)

    def run(self):
        """Take CLI arguments, parse it, and process."""
        self.validate_command()

        options = self.options

        show_version(options)
        show_info(options)

        # operation
        do_build_template(options)
        do_search_template(options)
        do_test_template(options)


def execute():
    """Execute template console CLI."""
    app = Cli()
    app.run()
