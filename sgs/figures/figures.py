# -*- coding: UTF-8 -*-

from sgs.constants import COUNTRIES, GENDERS, SKILL_STYLES
from sgs.misc import SgsCommandable


class FigureBase(SgsCommandable):
    """
    武将基类
    """
    def to_cmd_dict(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'hp': self.hp
        }


class CaoCao(FigureBase):
    """
    【曹操】 魏，男，4血
    【奸雄】【护驾】
    """
    def __init__(self):
        self.pk = 'WEI001'
        self.name = u'曹操'
        self.country = COUNTRIES.WEI
        self.gender = GENDERS.MALE
        self.hp = 4
        self.skills = {
            'WEI001s01': {
                'pk': 'WEI001s01',
                'style': SKILL_STYLES.NORMAL,
                'name': u'奸雄',
                'desc': u'你可以立即获得对你成伤害的牌。',
                'exec_fun': self._skill01},
            'WEI001s02': {
                'pk': 'WEI001s02',
                'style': SKILL_STYLES.ZHUGONG,
                'name': u'护驾',
                'desc': u'主公技，当你需要使用（或打出）一张【闪】时，'
                      + u'你可以发动护驾。所有“魏”势力角色按行动顺序依次选择是'
                      + u'否打出一张【闪】“提供”给你（然后视为由你使用或打出），'
                      + u'直到有—名角色或没有任何角色决定如此做时为止。',
                'exec_fun': self._skill02}
        }

    def _skill01(self):
        pass

    def _skill02(self):
        pass


class GuanYu(FigureBase):
    """
    【关羽】 蜀，男，4血
    【武圣】
    """
    def __init__(self):
        self.pk = 'SHU002'
        self.name = u'关羽'
        self.country = COUNTRIES.SHU
        self.gender = GENDERS.MALE
        self.hp = 4
        self.skills = {
            'SHU002s01': {
                'pk': 'SHU002s01',
                'style': SKILL_STYLES.NORMAL,
                'name': u'武圣',
                'desc': u'你可以将你的任意一张红色牌当【杀】使用或打出。',
                'exec_fun': self._skill01},
        }

    def _skill01(self):
        pass

    def _skill02(self):
        pass


class SiMaYi(FigureBase):
    """
    【司马懿】 蜀，男，3血
    【】
    """
    def __init__(self):
        self.pk = 'WEI002'
        self.name = u'司马懿'
        self.country = COUNTRIES.WEI
        self.gender = GENDERS.MALE
        self.hp = 3
        self.skills = {
            'WEI002s01': {
                'pk': 'WEI002s01',
                'style': SKILL_STYLES.NORMAL,
                'name': u'反馈',
                'desc': u'你可以立即从对你造成伤害的来源处获得一张牌。',
                'exec_fun': self._skill01},
            'WEI002s02': {
                'pk': 'WEI002s02',
                'style': SKILL_STYLES.NORMAL,
                'name': u'鬼才',
                'desc': u'在任意角色的判定牌生效前，你可以打出一张手牌代替之。',
                'exec_fun': self._skill02},
        }

    def _skill01(self):
        pass

    def _skill02(self):
        pass


class DaQiao(FigureBase):
    """
    【大乔】 吴，女，3血
    【】
    """
    def __init__(self):
        self.pk = 'WU006'
        self.name = u'大乔'
        self.country = COUNTRIES.WU
        self.gender = GENDERS.FEMALE
        self.hp = 3
        self.skills = {
            'WU006s01': {
                'pk': 'WU006s01',
                'style': SKILL_STYLES.NORMAL,
                'name': u'国色',
                'desc': u'出牌阶段，你可以将你任意方块花色的牌当【乐不思蜀】'
                      + u'使用。',
                'exec_fun': self._skill01},
            'WU006s02': {
                'pk': 'WU006s02',
                'style': SKILL_STYLES.NORMAL,
                'name': u'流离',
                'desc': u'当你成为【杀】的目标时，你可以弃一张牌，'
                      + u'并将此【杀】转移给你攻击范围内的另一名角色。'
                      + u'（该角色不得是【杀】的使用者）',
                'exec_fun': self._skill02},
        }

    def _skill01(self):
        pass

    def _skill02(self):
        pass


class XiaoQiao(FigureBase):
    """
    【小乔】 吴，女，3血
    【】
    """
    def __init__(self):
        self.pk = 'WU011'
        self.name = u'小乔'
        self.country = COUNTRIES.WU
        self.gender = GENDERS.FEMALE
        self.hp = 3
        self.skills = {
            'WU011s01': {
                'pk': 'WU011s01',
                'style': SKILL_STYLES.NORMAL,
                'name': u'天香',
                'desc': u'每当你受到伤害时，你可以弃一张红桃手牌来转移此伤'
                      + u'害给任意一名其他角色，然后该角色摸X张牌；X为该角色当前'
                      + u'已损失的体力值。',
                'exec_fun': self._skill01},
            'WU011s02': {
                'pk': 'WU011s02',
                'style': SKILL_STYLES.SUODING,
                'name': u'红颜',
                'desc': u'锁定技，你的黑桃牌均视为红桃牌。',
                'exec_fun': self._skill02},
        }

    def _skill01(self):
        pass

    def _skill02(self):
        pass


class ZhouTai(FigureBase):
    """
    【周泰】 吴，男，4血
    【】
    """
    def __init__(self):
        self.pk = 'WU013'
        self.name = u'周泰'
        self.country = COUNTRIES.WU
        self.gender = GENDERS.MALE
        self.hp = 4
        self.skills = {
            'WU013s01': {
                'pk': 'WU013s01',
                'style': SKILL_STYLES.SUODING,
                'name': u'不屈',
                'desc': u'任何时候，当你的体力被扣减到0或更低时，'
                      + u'每扣减1点体力：从牌堆亮出一张牌放在你的武将牌上，'
                      + u'若该牌的点数与你武将牌上已有的任何一张牌都不同，'
                      + u'你可以不死去。此牌亮出的时刻为你的濒死状态。',
                'exec_fun': self._skill01},
        }

    def _skill01(self):
        pass

    def _skill02(self):
        pass
