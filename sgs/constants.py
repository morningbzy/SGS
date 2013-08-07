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

COUNTRIES = Enum()
COUNTRIES.WEI = 1
COUNTRIES.SHU = 2
COUNTRIES.WU = 3
COUNTRIES.QUN = 4
COUNTRIES.SHEN = 5

GENDERS = Enum()
GENDERS.MALE = 0
GENDERS.FEMALE = 1

SKILL_STYLES = Enum()
SKILL_STYLES.NORMAL = 0
SKILL_STYLES.ZHUGONG = 1
SKILL_STYLES.SUODING = 2
SKILL_STYLES.XIANDING = 3
SKILL_STYLES.JUEXING = 3

CARD_CATEGORIES = Enum()
CARD_CATEGORIES.NORMAL = 0
CARD_CATEGORIES.JINNANG = 10
CARD_CATEGORIES.YANSHI_JINNANG = 11
CARD_CATEGORIES.WUQI = 20
CARD_CATEGORIES.FANGJU = 21
CARD_CATEGORIES.JIAYI = 22
CARD_CATEGORIES.JIANYI = 23

CARD_SUITS = Enum()
CARD_SUITS.HEI = 0
CARD_SUITS.HONG = 1
CARD_SUITS.MEI = 2
CARD_SUITS.FANG = 3
