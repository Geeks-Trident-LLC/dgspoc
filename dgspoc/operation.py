"""Module containing the logic for describe-get-system operation"""

import sys
import re

from dgspoc.utils import File
from dgspoc.utils import Printer

from dgspoc.config import Data

from dgspoc.usage import validate_usage
from dgspoc.usage import show_usage

from templateapp import TemplateBuilder


def do_build_template(options):
    command, operands = options.command, list(options.operands)
    op_count = len(operands)
    feature = str(operands[0]).lower().strip() if op_count > 0 else ''
    if command == 'build' and feature == 'template':
        operands = operands[1:]
        validate_usage('{}_{}'.format(command, feature), operands)

        op_txt = ' '.join(operands)

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
            print(factory.template)

            # tmpl_id = options.templateid.strip()
            # if tmpl_id:
            #     pattern = r'(?i)^overwrite_'
            #     is_overwritten = bool(re.match(pattern, tmpl_id))
            #     tmpl_id = re.sub(pattern, '', tmpl_id)
            #     with open(Data.template_storage_filename) as stream:
            #
            #     if is_overwritten:
            #         pass
            #     else:
            #         pass

            if options.filename:
                is_saved = File.save(options.filename, factory.template)
                print('\n{}\n'.format(Printer.get(File.message)))
                if not is_saved:
                    sys.exit(1)
            sys.exit(0)
        except Exception as ex:
            print('*** {}: {}'.format(type(ex).__name__, ex))
            sys.exit(1)
