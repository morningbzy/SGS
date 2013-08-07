# -*- coding: UTF-8 -*-

import logging
from random import randint

from sgs.card import global_cards
from sgs.cmd import Cmd
from sgs.constants import ROLE_LABELS
from sgs.constants import ROLES
from sgs.figure import global_figures
from sgs.user import global_users


class Game(object):
    pass


class Phase(object):
    pass


class SgsGame(Game, Phase):
    c = 0
    cmd_list = []

    def __init__(self):
        self.game_board = SgsGameBoard()
        super(SgsGame, self).__init__()
        self.cmd_mapping = {
            'JOIN': self._join,
            'READY': self._ready,
            'UNREADY': self._unready,
        }
        self.wait_callback = None
        self.wait_args = None
        self.wait_kwargs = None

    #-------------游戏阶段-------------
    def start(self):
        # 游戏开始
        global_users.broadcast_cmd(Cmd('GAME_START'))
        global_users.broadcast_cmd(Cmd('GAME_MSG', msg=u'游戏开始，分配角色'))
        # 分配角色
        roles = self.game_board.get_roles()
        for u in global_users.users.itervalues():
            r = roles.pop(randint(0, len(roles) - 1))
            self.game_board.set_role(u, r)
        zhugong = self.game_board.zhugong
        global_users.broadcast_cmd(
            Cmd('SHOW_ROLE',
                seat_id=zhugong.seat_id,
                label=ROLE_LABELS[zhugong.role]))
        # 分配武将
        #class ChooseFigurePhase(Phase):
        #    next_phases = [
        #        ZhugongChooseFigurePhase
        #        OtherChooseFigurePhase]
        # 主公选将
        #class ZhugongChooseFigurePhase(Phase):
        global_users.broadcast_cmd(Cmd('GAME_MSG', msg=u'等待主公选择武将'))
        candidates = global_figures.take_zhugong_figures()
        self.game_board.zhugong.add_cmd(
            Cmd('SET_FIGURE_CANDIDATE',
                figures=[c.to_cmd_dict() for c in candidates]))
        global_figures.remove_used(candidates)
        self.wait(self._on_zhugong_choose_figure, candidates=candidates)

    def _on_zhugong_choose_figure(self, cmd):
        """
        等待主公选择武将
        """
        zhugong = global_users.get_user(cmd.sender)
        if zhugong.role != ROLES.ZHUGONG or cmd.cmd != "CHOOSE_FIGURE":
            return
        zhugong.set_figure(global_figures.figures[cmd.figure_id])
        global_figures.add_used([cmd.figure_id])
        global_users.broadcast_cmd(
            Cmd('SHOW_FIGURE',
                seat_id=zhugong.seat_id,
                figures=[zhugong.figure.to_cmd_dict()]))
        self.reset_wait_callback()
        # 其他人选将
        #class OtherChooseFigurePhase(Phase):
        all_candidates = []
        for user in self.game_board.one_round(except_user=[zhugong.pk]):
            candidates = global_figures.take_random_figure(count=2)
            all_candidates.extend(candidates)
            user.add_cmd(
                Cmd('SET_FIGURE_CANDIDATE',
                    figures=[c.to_cmd_dict() for c in candidates]))
        global_figures.remove_used(all_candidates)
        self.wait(self._on_other_choose_figure,
                  all_candidates=all_candidates)

    def _on_other_choose_figure(self, cmd):
        """
        等待其他玩家选择武将
        """
        user = global_users.get_user(cmd.sender)
        if user.figure is None:
            user.set_figure(global_figures.figures[cmd.figure_id])
            global_figures.add_used([cmd.figure_id])
        if not self.game_board.is_all_chosen_figure():
            return
        self.reset_wait_callback()
        # 所有人亮武将
        for user in self.game_board.one_round():
            global_users.broadcast_cmd(
                Cmd('SHOW_FIGURE',
                    seat_id=user.seat_id,
                    figures=[user.figure.to_cmd_dict()]))
        # 每人首发4张牌
        for user in self.game_board.one_round():
            cards = global_cards.get_cards(count=4)
            user.set_cards(cards)
            global_users.broadcast_cmd(
                Cmd('GAIN_CARD', seat_id=user.seat_id, count=4))

    #----------------------------------

    def wait(self, callback, *args, **kwargs):
        logging.info('[W] %s' % callback.__doc__.strip())
        self.wait_callback = callback
        self.wait_args = args
        self.wait_kwargs = kwargs

    def reset_wait_callback(self):
        self.wait_callback = None
        self.wait_args = None
        self.wait_kwargs = None

    def handle_cmd(self, cmd):
        if self.wait_callback:
            self.wait_callback(cmd)

        elif cmd.cmd in self.cmd_mapping:
            self.cmd_mapping[cmd.cmd](cmd)

    def _join(self, cmd):
        user = global_users.get_user(cmd.sender)
        if user.seat_id is None:
            seat_id = self.game_board.get_random_seat()
            if seat_id != -1:
                user.seat_id = seat_id
                self.game_board.join(seat_id, user)
                cmd.update_args({'seat_id': seat_id,
                                 'max_seat': self.game_board.MAX_SEAT})
                global_users.broadcast_cmd(cmd)
        else:
            user.restore()  # 恢复用户游戏状态
        for seat, u in self.game_board.seats.iteritems():
            if u.pk == user.pk:
                continue
            user.add_cmd(Cmd('JOIN', sender=u.pk, seat_id=seat))
            if u.is_ready:
                user.add_cmd(Cmd('READY', sender=u.pk, seat_id=seat))

    def _ready(self, cmd):
        user = global_users.get_user(cmd.sender)
        user.is_ready = True
        global_users.broadcast_cmd(cmd)

        if self.game_board.is_all_ready():
            self.start()

    def _unready(self, cmd):
        user = global_users.get_user(cmd.sender)
        user.is_ready = False
        global_users.broadcast_cmd(cmd)


class GameBoard(object):
    pass


class SgsGameBoard(object):
    MAX_SEAT = 2

    def __init__(self):
        self.seats = {}
        self.roles = {
            ROLES.ZHUGONG: [],
            ROLES.FANZEI: [],
            ROLES.ZHONGCHEN: [],
            ROLES.NEIJIAN: []
        }

    def get_random_seat(self):
        for i in xrange(self.MAX_SEAT):
            if i not in self.seats:
                self.seats[i] = None
                return i
        return -1

    def join(self, seat_id, user):
        assert self.seats[seat_id] is None, "座位被占"
        self.seats[seat_id] = user

    def leave(self, seat_id, user):
        assert self.seats[seat_id].pk == user.pk, "不是他"
        self.seats.pop(seat_id)

    def is_all_ready(self):
        if len(self.seats) < self.MAX_SEAT:
            return False
        for u in self.seats.itervalues():
            if not u.is_ready:
                return False
        return True

    def is_all_chosen_figure(self):
        for u in self.seats.itervalues():
            if not u.figure:
                return False
        return True

    def get_roles(self):
        roles_mapping = {
            2: [ROLES.ZHUGONG, ROLES.FANZEI],
            3: [ROLES.ZHUGONG, ROLES.FANZEI, ROLES.NEIJIAN]
            #TODO 多人
        }
        return roles_mapping[self.MAX_SEAT]

    def set_role(self, user, role):
        user.set_role(role)
        self.roles[role].append(user)

    def get_role(self, role):
        return self.roles[role]

    @property
    def zhugong(self):
        return self.roles[ROLES.ZHUGONG][0]

    def one_round(self, start=None, except_user=[]):
        start = self.zhugong.seat_id if start is None else start
        for i in xrange(self.MAX_SEAT):
            u = self.seats[(start + i) % self.MAX_SEAT]
            if u.pk in except_user:
                continue
            yield u


global_game = SgsGame()
