"""Module containing the logic for describe-get-system proof of conception entry-points."""

import sys
import argparse

from dgspoc import version
from dgspoc.config import Data
from dgspoc.utils import Printer


def show_dependency(options):
    if options.command == 'dependency':
        lst = [
            'Describe-Get-System Proof of Concept',
            Data.get_app_info(),
            '--------------------',
            'Dependencies:'
        ]

        for pkg in Data.get_dependency().values():
            lst.append('  + Package: {0[package]}'.format(pkg))
            lst.append('             {0[url]}'.format(pkg))

        Printer.print(lst)
        sys.exit(0)


def show_info(options):
    if options.command == 'info':
        lst = [
            'Describe-Get-System Proof of Concept',
            Data.get_app_info(),
            '--------------------',
            'Dependencies:'
        ]

        for pkg in Data.get_dependency().values():
            lst.append('  + Package: {0[package]}'.format(pkg))
            lst.append('             {0[url]}'.format(pkg))

        Printer.print(lst)
        sys.exit(0)


def show_version(options):
    if options.command == 'version':
        print('{} {}'.format(Cli.prog, version))
        sys.exit(0)


class Cli:
    """describe-get-system proof of concept console CLI application."""
    prog = 'dgs'
    prog_fn = 'describe-get-system'
    commands = ['build', 'check', 'dependency',
                'info', 'run', 'test', 'version']

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
            'command', type=str,
            help='command must be either build, check,'
                 'dependency, info, run, test, or version'
        )
        parser.add_argument(
            'operands', nargs='*', type=str,
            help='operands can be template, unittest, '
                 'pytest, robotframework, script, or data such command-line, '
                 'config-lines, or filename'
        )

        self.parser = parser
        self.options = self.parser.parse_args()
        self.kwargs = dict()

    def validate_command(self):
        """Validate argparse `options.command`.

        Returns
        -------
        bool: show ``self.parser.print_help()`` and call ``sys.exit(1)`` if
        command is neither build, check, dependency, info, run,
        test, nor version, otherwise, return True
        """
        self.options.command = self.options.command.lower()

        if self.options.command in self.commands:
            return True
        self.parser.print_help()
        sys.exit(1)

    def run(self):
        """Take CLI arguments, parse it, and process."""
        self.validate_command()
        show_version(self.options)
        show_dependency(self.options)
        show_info(self.options)


def execute():
    """Execute template console CLI."""
    app = Cli()
    app.run()
