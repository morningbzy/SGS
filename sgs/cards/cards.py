# -*- coding: UTF-8 -*-

from sgs.misc import SgsCommandable


class CardBase(SgsCommandable):
    """
    卡牌基类
    """
    def to_cmd_dict(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'category': self.category,
            'suit': self.suid,
            'number': self.number
        }


class Sha(CardBase):
    pass
