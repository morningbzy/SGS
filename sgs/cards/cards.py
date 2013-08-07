# -*- coding: UTF-8 -*-

from sgs.constants import CARD_CATEGORIES
from sgs.constants import CARD_SUITS
from sgs.misc import SgsCommandable


class CardBase(SgsCommandable):
    """
    卡牌基类
    """
    name = NotImplemented
    category = NotImplemented

    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def to_cmd_dict(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'category': self.category,
            'suit': self.suit,
            'number': self.number
        }


class JibenCard(CardBase):
    category = CARD_CATEGORIES.NORMAL


class Sha(JibenCard):
    name = u'杀'


class Shan(JibenCard):
    name = u'闪'


class Tao(JibenCard):
    name = u'桃'


_cards = [
    Sha(CARD_SUITS.HEI, 10),
    Sha(CARD_SUITS.HEI, 10),
    Sha(CARD_SUITS.HONG, 10),
    Sha(CARD_SUITS.MEI, 3),
    Sha(CARD_SUITS.MEI, 6),
    Sha(CARD_SUITS.MEI, 9),
    Sha(CARD_SUITS.MEI, 10),
    Sha(CARD_SUITS.FANG, 9),

    Shan(CARD_SUITS.FANG, 2),
    Shan(CARD_SUITS.FANG, 4),
    Shan(CARD_SUITS.FANG, 8),
    Shan(CARD_SUITS.FANG, 11),

    Tao(CARD_SUITS.HONG, 5),
    Tao(CARD_SUITS.HONG, 7),
    Tao(CARD_SUITS.FANG, 2),
]

all_cards = {}
for i, card in enumerate(_cards):
    card.pk = i
    all_cards[i] = card
print all_cards
