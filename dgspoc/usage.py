"""Module containing the logic for console command line usage"""

import sys

from dgspoc.utils import Printer
from dgspoc.utils import Misc


class BuildUsage:
    usage = '\n'.join([
        'build command has two features: template or script',
        'common optional arguments:',
        "  -a AUTHOR, --author AUTHOR               author's name",
        "  -e EMAIL, --email EMAIL                  author's email",
        "  -c COMPANY, --company COMPANY            author's company",
        "  -s FILENAME, --save FILENAME             save to file",
        "  --replaced                               overwrite template ID/file",
        '',
        'build template syntax:',
        '----------------------',
        'optional arguments:',
        "  -i TMPLID, --template-id TMPLID          template ID",
        '----------------------',
        'dgs build template "<single_line_snippet>" [options]',
        'dgs build template <snippet_filename> [options]',
        'dgs build template example {1, 2, 3, 4, or 5}',
        '',
        'build script syntax:',
        '----------------------',
        'optional arguments:',
        "  -w FRAMEWORK, --framework FRAMEWORK      test framework",
        "  -r RESOURCE --resource RESOURCE          test resource",
        '----------------------',
        'dgs build script <snippet_filename> [options]',
        'dgs build script example {1, 2, or 3}'
    ])


class BuildTemplateUsage:
    usage = '\n'.join([
        'build template syntax:',
        '----------------------',
        'optional arguments:',
        "  -a AUTHOR, --author AUTHOR               author's name",
        "  -e EMAIL, --email EMAIL                  author's email",
        "  -c COMPANY, --company COMPANY            author's company",
        "  -s FILENAME, --save FILENAME             save to file",
        "  -i TMPLID, --template-id TMPLID          template ID",
        "  --replaced                               overwrite template ID/file",
        '----------------------',
        'dgs build template "<single_line_snippet>" [options]',
        'dgs build template <snippet_filename> [options]',
        'dgs build template example {1, 2, 3, 4, or 5}',
    ])

    other_usage = '\n'.join([
        'build template example syntax:',
        '----------------------',
        'dgs build template example 1',
        'dgs build template example 2',
        'dgs build template example 3',
        'dgs build template example 4',
        'dgs build template example 5',
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


class SearchTemplateUsage:
    usage = '\n'.join([
        'search template syntax:',
        'Note: template-id pattern should allow wildcard matching',
        '-----------------------',
        'optional arguments:',
        "  --ignore-case                            case insensitive matching",
        "  --showed                                 showing template",
        '----------------------',
        'dgs search template "<template-id-pattern>" [options]',
        'dgs search template example {1, 2, or 3}',
    ])

    other_usage = '\n'.join([
        'search template example syntax:',
        '----------------------',
        'dgs search template example 1',
        'dgs search template example 2',
        'dgs search template example 3',
    ])


class Usage:
    build = BuildUsage
    build_template = BuildTemplateUsage
    info = InfoUsage
    search_template = SearchTemplateUsage


def validate_usage(name, operands):
    result = ''.join(operands) if Misc.is_list_instance(operands) else str(operands)
    if result.strip().lower() == 'usage':
        show_usage(name, exit_code=0)


def show_usage(name, *args, exit_code=None):
    obj = getattr(Usage, name, None)
    if getattr(obj, 'usage', None):
        attr = '_'.join(list(args) + ['usage'])
        Printer.print(getattr(obj, attr))
        Misc.is_integer(exit_code) and sys.exit(exit_code)
    else:
        fmt = '*** ErrorUsage: "{}" has not defined or unavailable.'
        print(fmt.format(name))
        sys.exit(1)


def get_global_usage():
    lst = [
    ]

    return '\n'.join(lst)