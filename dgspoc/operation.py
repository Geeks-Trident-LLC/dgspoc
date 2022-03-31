"""Module containing the logic for describe-get-system operation"""

import sys
import re

from dgspoc.utils import File
from dgspoc.utils import Printer
from dgspoc.utils import Text

from dgspoc.utils import ECODE

from dgspoc.storage import TemplateStorage

from dgspoc.example import BuildTemplateExample
from dgspoc.example import SearchTemplateExample
from dgspoc.example import TestTemplateExample

from dgspoc.usage import validate_usage
from dgspoc.usage import show_usage

from dgspoc.adaptor import Adaptor

from templateapp import TemplateBuilder

from io import StringIO
from textfsm import TextFSM
from pprint import pprint
from dlapp.collection import Tabular


def do_build_template(options):
    command, operands = options.command, list(options.operands)
    op_count = len(operands)
    feature = str(operands[0]).lower().strip() if op_count > 0 else ''
    if command == 'build' and feature == 'template':
        operands = operands[1:]
        validate_usage('{}_{}'.format(command, feature), operands)

        op_txt = ' '.join(operands).rstrip()

        if not op_txt:
            show_usage('{}_{}'.format(command, feature), exit_code=ECODE.BAD)
        elif op_txt.lower().startswith('example'):
            index = str(operands[-1]).strip()
            if op_count == 3 and re.match('[1-5]$', index):
                result = BuildTemplateExample.get(index)
                Printer.print_message('\n\n{}\n', result)
                sys.exit(ECODE.SUCCESS)
            else:
                show_usage('{}_{}'.format(command, feature), 'other', exit_code=ECODE.BAD)

        if File.is_exist(op_txt):
            with open(op_txt) as stream:
                user_data = stream.read()
        else:
            user_data = op_txt

        try:
            factory = TemplateBuilder(
                user_data=user_data, author=options.author, email=options.email,
                company=options.company
            )

            template_id = options.tmplid.strip()
            filename = options.filename.strip()

            fmt1 = '+++ Successfully uploaded generated template to "{}" template ID.'
            fmt2 = '+++ Successfully saved generated template to {}'
            fmt3 = 'CANT save generated template to existing {} file.  Use replaced flag accordingly.'

            if template_id or filename:
                is_ok = True
                lst = []
                if template_id:
                    is_uploaded = TemplateStorage.upload(
                        template_id, factory.template, replaced=options.replaced
                    )
                    is_ok &= is_uploaded
                    msg = fmt1.format(template_id) if is_uploaded else TemplateStorage.message
                    lst.append(msg)
                if filename:
                    filename = File.get_path(filename)
                    if File.is_exist(filename) and not options.replaced:
                        msg = fmt3.format(filename)
                        is_ok &= False
                    else:
                        is_saved = File.save(options.filename, factory.template)
                        is_ok &= is_saved
                        msg = fmt2.format(filename) if is_saved else File.message

                    lst and lst.append('=' * 20)
                    lst.append(msg)

                lst and Printer.print(lst)
                sys.exit(ECODE.SUCCESS if is_ok else ECODE.BAD)
            else:
                print(factory.template)
                sys.exit(ECODE.SUCCESS)

        except Exception as ex:
            print(Text(ex))
            sys.exit(ECODE.BAD)

    elif command == 'build' and feature != 'template':
        if feature == 'script':
            return
        else:
            exit_code = ECODE.SUCCESS if feature == 'usage' else ECODE.BAD
            show_usage(command, exit_code=exit_code)


def do_search_template(options):
    command, operands = options.command, list(options.operands)
    op_count = len(operands)
    feature = str(operands[0]).lower().strip() if op_count > 0 else ''
    if command == 'search' and feature == 'template':
        operands = operands[1:]
        validate_usage('{}_{}'.format(command, feature), operands)

        op_txt = ' '.join(operands).rstrip()

        if not op_txt:
            show_usage('{}_{}'.format(command, feature), exit_code=ECODE.BAD)
        elif op_txt.lower().startswith('example'):
            index = str(operands[-1]).strip()
            if op_count == 3 and re.match('[1-3]$', index):
                result = SearchTemplateExample.get(index)
                Printer.print_message('\n\n{}\n', result)
                sys.exit(ECODE.SUCCESS)
            else:
                show_usage('{}_{}'.format(command, feature), 'other', exit_code=ECODE.BAD)

        tmpl_id_pattern = operands[0]
        is_found = TemplateStorage.search(tmpl_id_pattern,
                                          ignore_case=options.ignore_case,
                                          showed=options.showed)
        print(TemplateStorage.message)
        sys.exit(ECODE.SUCCESS if is_found else ECODE.BAD)

    elif command == 'search' and feature != 'template':
        exit_code = ECODE.SUCCESS if feature == 'usage' else ECODE.BAD
        show_usage('{}_template'.format(command), exit_code=exit_code)


def do_test_template(options):
    command, operands = options.command, list(options.operands)
    op_count = len(operands)
    feature = str(operands[0]).lower().strip() if op_count > 0 else ''
    if command == 'test' and feature == 'template':
        operands = operands[1:]
        validate_usage('{}_{}'.format(command, feature), operands)

        op_txt = ' '.join(operands).rstrip()

        if not op_txt:
            show_usage('{}_{}'.format(command, feature), exit_code=ECODE.BAD)
        elif op_txt.lower().startswith('example'):
            index = str(operands[-1]).strip()
            if op_count == 3 and re.match('[1-3]$', index):
                result = TestTemplateExample.get(index)
                Printer.print_message('\n\n{}\n', result)
                sys.exit(ECODE.SUCCESS)
            else:
                show_usage('{}_{}'.format(command, feature), 'other', exit_code=ECODE.BAD)
        else:
            if options.testfile == '' and options.adaptor == '':
                lst = ['CANT run template test WITHOUT test data.',
                       'Please use --test-file=<test-file-name> or',
                       '           --adaptor=<adaptor_name> --execution="<device cmdline>"']
                Printer.print(lst)
                show_usage('{}_{}'.format(command, feature), exit_code=ECODE.BAD)

        test_data = ''
        if options.adaptor:
            try:
                pattern = r'((host|testcase)::(\S+))'
                cmdline = re.sub(pattern, '', options.execution, re.I).strip()
                tbl = dict()
                for _, key, val in re.findall(pattern, options.execution):
                    tbl[key.lower()] = val

                host, testcase = tbl.get('host', ''), tbl.get('testcase', '')
                if not host:
                    lst = [
                        'ExecutionSyntaxError: must be',
                        '--execution="host::<addr_or_name> <cmdline>"',
                        '--execution="host::<addr_or_name> testcase::<tc_name> <cmdline>"'
                    ]
                    Printer.print(lst)
                    show_usage('{}_{}'.format(command, feature), exit_code=ECODE.BAD)

                device = Adaptor(options.adaptor, host, testcase=testcase)
                device.connect()
                test_data = device.execute(cmdline)
                device.disconnect()
                device.release()
            except Exception as ex:
                failure = 'AdaptorInquiryError - ({})'.format(Text(ex))
                Printer.print(failure)
                sys.exit(ECODE.BAD)
        elif options.testfile:
            if File.is_exist(options.testfile):
                test_data = open(options.testfile).read()
            else:
                fmt = '*** "{}" test data file is NOT existed.'
                failure = fmt.format(options.testfile)
                Printer.print(failure)
                sys.exit(ECODE.BAD)

        tmpl_id = operands[0]
        fn = tmpl_id
        template = ''
        if TemplateStorage.check(tmpl_id):
            template = TemplateStorage.get(tmpl_id)
        elif File.is_exist(fn):
            template = open(fn).read()

        if not template:
            lst = [
                '"{}" is NOT template ID or template filename.'.format(tmpl_id),
                'Please provide the valid template_id or template_file'
            ]
            Printer.print(lst)
            sys.exit(ECODE.BAD)

        try:
            stream = StringIO(template)
            parser = TextFSM(stream)
            rows = parser.ParseTextToDicts(test_data)
            if rows:
                lst = [
                    'Result:'
                    '+++ Template parsed {} record(s).'.format(len(rows))
                ]
            else:
                lst = [
                    'Result:'
                    '*** Template could NOT find and parse any record.'
                ]

            if options.showed:
                Printer.print('Test Data:')
                print(test_data)
                print()
                Printer.print('Template:')
                print(template)
                print()
            Printer.print(lst)
            Tabular(rows).print() if options.tabular else pprint(rows)

            sys.exit(ECODE.SUCCESS)
        except Exception as ex:
            failure = 'BAD-TEMPLATE ({})'.format(Text(ex))
            Printer.print(failure)
            sys.exit(ECODE.BAD)

    elif command == 'test' and feature != 'template':
        if feature == 'execution':
            return
        exit_code = ECODE.SUCCESS if feature == 'usage' else ECODE.BAD
        show_usage('{}_template'.format(command), exit_code=exit_code)
