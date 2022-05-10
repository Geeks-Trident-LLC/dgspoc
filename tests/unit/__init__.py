import re


class ReformatOutput:
    def __init__(self, raw_data):
        self.device_name = ''
        self.raw_data = str(raw_data)
        self.output = ''
        self.process()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            chk = self.output == other.output
            return chk
        elif isinstance(other, str):
            new_other = other.replace('{device_name}', self.device_name)
            chk = self.output == new_other
            return chk
        return False

    def __repr__(self):
        return self.output

    def __str__(self):
        return self.output

    def process(self):
        if self.raw_data.strip() == '':
            return

        lines = self.raw_data.splitlines()
        lst = []
        pat1 = r'(?i)- UNREAL-DEVICE-[a-z]+-SERVICE-TIMESTAMP'
        pat2 = r'(?i)(?P<name>\S+) +is +(successfully +)?((dis)?connected)[.]'
        for line in lines:
            if re.search(pat1, line):
                continue
            lst.append(line)
            match = re.match(pat2, line)
            if match and not self.device_name:
                self.device_name = match.group('name')

        self.output = '\n'.join(lst)
