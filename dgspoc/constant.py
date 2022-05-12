"""Module containing the logic for constant definition"""

import re
from enum import IntFlag


class ICSValue:
    """Treating value as ignore case and ignore space during evaluating
    string equality"""
    def __init__(self, value, equality='', is_strip=False):
        self.value = str(value)
        self.equality = equality
        self.is_strip = is_strip

    def __eq__(self, other):
        value1 = self.value.lower()

        if isinstance(other, self.__class__):
            value2 = other.value.lower()
        else:
            value2 = str(other).lower()

        value1 = re.sub(' +', ' ', value1)
        value2 = re.sub(' +', ' ', value2)

        if self.is_strip:
            value1 = value1.strip()
            value2 = value2.strip()

        if self.equality:
            if isinstance(self.equality, (list, tuple)):
                is_equal = True
                for item in self.equality:
                    item = str(item)
                    try:
                        is_equal = bool(re.match(item, value2, re.I))
                    except Exception as ex:     # noqa
                        item = re.sub(' +', ' ', item.lower())
                        is_equal &= item == value2
                return is_equal
            else:
                pattern = str(self.equality)
                try:
                    is_equal = bool(re.match(pattern, value2, re.I))
                except Exception as ex:     # noqa
                    equality = re.sub(' +', ' ', str(self.equality).lower())
                    is_equal = equality == value2
                return is_equal
        else:
            chk = value1.strip() == value2.strip()
        return chk

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return self.value


class ECODE(IntFlag):
    SUCCESS = 0
    BAD = 1


class FWTYPE:
    UNITTEST = ICSValue('unittest')
    PYTEST = ICSValue('pytest')
    ROBOTFRAMEWORK = ICSValue('robotframework', equality=r'(rf|robotframework)$')


class CONVTYPE:
    CSV = ICSValue('csv')
    JSON = ICSValue('json')
    TEMPLATE = ICSValue('template')


class COMMAND:
    BUILD = ICSValue('build')
    INFO = ICSValue('info')
    RUN = ICSValue('run')
    SEARCH = ICSValue('search')
    TEST = ICSValue('test')
    VERSION = ICSValue('version')
    USAGE = ICSValue('usage')
