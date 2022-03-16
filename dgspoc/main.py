"""Module containing the logic for describe-get-system proof of conception entry-points."""

import sys
import argparse

from dgspoc import version


def show_dependency(options):
    if options.dependency:
        from platform import uname, python_version
        from dgspoc.config import Data
        lst = [
            Data.main_app_text,
            'Platform: {0.system} {0.release} - Python {1}'.format(
                uname(), python_version()
            ),
            '--------------------',
            'Dependencies:'
        ]

        for pkg in Data.get_dependency().values():
            lst.append('  + Package: {0[package]}'.format(pkg))
            lst.append('             {0[url]}'.format(pkg))

        width = max(len(item) for item in lst)
        txt = '\n'.join('| {1:{0}} |'.format(width, item) for item in lst)
        print('+-{0}-+\n{1}\n+-{0}-+'.format(width * '-', txt))
        sys.exit(0)


class Cli:
    """describe-get-system proof of concept console CLI application."""
    prog = 'dgs'
    prog_fn = 'describe-get-system'
    commands = ['build', 'check', 'config', 'create', 'execute',
                'info', 'reset', 'upload', 'version']

    def __init__(self):
        parser = argparse.ArgumentParser(
            prog=self.prog,
            usage='%(prog)s [options] command operands',
            description='{} proof of concept'.format(self.prog_fn),
        )

        parser.add_argument(
            '-d', '--dependency', action='store_true',
            help='show {} dependent package(s)'.format(self.prog_fn)
        )

        parser.add_argument(
            '-v', '--version', action='version',
            version='%(prog)s v{}'.format(version)
        )

        parser.add_argument(
            'command', type=str,
            help='command must be either version, info, create, reset, check,'
                 'upload, config, or build'
        )
        parser.add_argument(
            'operands', nargs='*', type=str,
            help='operands can be mockdevice, template, unittest, '
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
        command is not version, info, create, reset, check, upload, config,
        or build, otherwise, return True
        """
        if self.options.command.lower() in self.commands:
            return True
        self.parser.print_help()
        sys.exit(1)

    def run(self):
        """Take CLI arguments, parse it, and process."""
        show_dependency(self.options)
        self.validate_command()


def execute():
    """Execute template console CLI."""
    app = Cli()
    app.run()
