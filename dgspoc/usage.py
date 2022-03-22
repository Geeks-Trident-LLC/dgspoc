"""Module containing the logic for console command line usage"""

import sys

from dgspoc.utils import Printer


class BuildTemplateUsage:
    usage = '\n'.join([
        'build template syntax:',
        '----------------------',
        'dgs build template "<single_line_snippet>"',
        'dgs build template <snippet_filename>',
    ])


class InfoUsage:
    usage = '\n'.join([
        'info syntax:',
        '------------',
        'dgs info',
        'dgs info all',
        'dgs info dependency',
        'dgs info template'
    ])


class Usage:
    build_template = BuildTemplateUsage
    info = InfoUsage


def validate_usage(name, operands):
    result = ''.join(operands) if isinstance(operands, list) else str(operands)
    if result.strip().lower() == 'usage':
        show_usage(name)


def show_usage(name, *args):
    obj = getattr(Usage, name, None)
    if getattr(obj, 'usage', None):
        attr = '_'.join(list(args) + ['usage'])
        Printer.print(getattr(obj, attr))
        sys.exit(0)
    else:
        fmt = '***Usage of "{}" has not defined or unavailable.'
        print(fmt.format(name))
        sys.exit(1)


def get_global_usage():
    lst = [
    ]

    return '\n'.join(lst)