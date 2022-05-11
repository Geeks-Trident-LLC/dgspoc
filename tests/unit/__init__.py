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
        excluded_txt_pat = r'^ERROR: .+? [<>=]{1,2} .+?$'
        service_stamp_pat = r'(?i)- UNREAL-DEVICE-[a-z]+-SERVICE-TIMESTAMP'
        replacing_service_stamp_pat = r'(?i)^[a-z]{3} \d{2} \d{4} \d{2}:\d{2}:\d{2}[.]\d{3}'
        replacing_created_date_pat = r'(?i)^(# Created date:) (\d{4}-\d\d-\d\d)( *)$'

        device_name_pat = r'(?i)(?P<name>\S+) +is +(successfully +)?((dis)?connected)[.]'
        for line in lines:
            if re.match(excluded_txt_pat, line):
                continue
            elif re.search(service_stamp_pat, line):
                changed_txt = re.sub(replacing_service_stamp_pat,
                                     'mmm dd yyyy HH:MM:SS.###', line)
                lst.append(changed_txt)
            elif re.match(replacing_created_date_pat, line):
                changed_txt = re.sub(replacing_created_date_pat,
                                     r'\1 yyyy-mm-dd\3', line)
                lst.append(changed_txt)
            else:
                lst.append(line)
                match = re.match(device_name_pat, line)
                if match and not self.device_name:
                    self.device_name = match.group('name')

        self.output = '\n'.join(lst)
