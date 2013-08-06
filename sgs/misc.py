
import re


def smart_lower(s):
    return '_'.join(re.findall(r'[A-Z][^A-Z]*', s)).lower()


class SgsCommandable(object):
    def to_cmd_dict(self):
        return {}
