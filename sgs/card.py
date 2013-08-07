# -*- coding: UTF-8 -*-

import random

from sgs.cards.cards import CardBase
from sgs.cards.cards import all_cards


class SgsCard(object):
    def __init__(self):
        self.cards = all_cards  # 所有的卡牌
        self.unused = []  # 摸牌堆
        self.used = all_cards.keys()  # 弃牌堆的卡牌
        self.onhand = []  # 玩家正在使用的卡牌

    def shuffle(self):
        """
        将弃牌堆并入摸牌堆，并洗牌
        """
        self.unused += self.used
        random.shuffle(self.unused)
        self.used = []

    def get_cards(self, count=1):
        """
        从摸牌堆顶摸牌
        """
        # 牌不够，则回收弃牌堆，洗牌
        if count > len(self.unused):
            self.shuffle()
        assert len(self.unused) > count, u'牌不够了'

        cards = self.unused[:count]
        self.unused = self.unused[count:]
        self.onhand.extend(cards)
        return [self.cards[k] for k in cards]

    def put_cards(self, cards, bottom=False):
        """
        放回摸牌堆
        """
        cards = [c.pk if isinstance(c, CardBase) else c for c in cards]
        if bottom:
            self.unused.extend(cards)
        else:
            cards.extend(self.unused)
            self.unused = cards

    def use_cards(self, cards):
        """
        置入弃牌堆
        """
        self.used([c.pk if isinstance(c, CardBase) else c for c in cards])


global_cards = SgsCard()
