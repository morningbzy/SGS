# -*- coding: UTF-8 -*-

from UserDict import UserDict


class Enum(object):
    pass


class FancyDict(UserDict):
    def __getattr__(self, key):
        try:
            return self.data[key]
        except KeyError, e:
            raise(AttributeError, e)


ROLES = Enum()
ROLES.ZHUGONG = 0  # FancyDict(pk=0, label=u'主公')
ROLES.FANZEI = 1  # FancyDict(pk=1, label=u'反贼')
ROLES.ZHONGCHEN = 2  # FancyDict(pk=2, label=u'忠臣')
ROLES.NEIJIAN = 3  # FancyDict(pk=3, label=u'内奸')

ROLE_LABELS = {
    ROLES.ZHUGONG: u'主公',
    ROLES.FANZEI: u'反贼',
    ROLES.ZHONGCHEN: u'忠臣',
    ROLES.NEIJIAN: u'内奸',
}
