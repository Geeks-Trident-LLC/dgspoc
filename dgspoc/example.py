"""Module containing the logic for console command line examples"""

from yaml import safe_load
from pathlib import Path
from dgspoc.utils import Printer


class Example:
    name = 'example'

    @classmethod
    def get(cls, index):
        file_obj = Path(Path(__file__).parent, 'exampledata.yaml')
        content = file_obj.read_text()
        dict_obj = safe_load(content)
        node = dict_obj.get(cls.name).get('example{}'.format(index))
        header = node.get('header')
        header = Printer.get(header)
        body = node.get('body')
        example_text = '{}\n\n{}'.format(header, body)
        return example_text


class BuildTemplateExample(Example):
    name = 'build_template'


class SearchTemplateExample(Example):
    name = 'search_template'
