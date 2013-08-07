# -*- coding: UTF-8 -*-

import logging

from sgs.cmd import Cmd
from sgs.constants import ROLE_LABELS


class User(object):
    def __init__(self, pk, **args):
        self.pk = pk
        self.cmd_waiter = None
        self.cmd_cache = []
        self.__dict__.update(args)
        self.seat_id = None
        self.is_ready = False
        self.role = None
        self.figure = None
        self.cards = []

    def get_cmds(self, callback):
        if self.cmd_cache:
            cmd = self.cmd_cache[0]
            callback(cmd)
            logging.info('--> [%s][%s] %s' % (self.pk, cmd.cmd, cmd))
            self.cmd_cache = self.cmd_cache[1:]
            return
        self.cmd_waiter = callback

    def cancel_wait(self):
        self.cmd_waiter = None

    def add_cmd(self, cmd):
        self.cmd_cache.append(cmd)
        if self.cmd_waiter:
            try:
                cmd = self.cmd_cache[0]
                self.cmd_waiter(cmd)
                logging.info('--> [%s][%s] %s' % (self.pk, cmd.cmd, cmd))
                self.cmd_waiter = None
                self.cmd_cache = self.cmd_cache[1:]
            except:
                logging.error('Error in waiter callback', exc_info=True)

    def resend_cmd(self, cmd):
        self.cmd_cache.insert(0, cmd)

    def restore(self):
        self.add_cmd(Cmd('JOIN',
                         sender=self.pk,
                         seat_id=self.seat_id))
        if self.is_ready:
            self.add_cmd(Cmd('READY',
                             sender=self.pk,
                             seat_id=self.seat_id))
        if self.role:
            self.add_cmd(Cmd('SET_ROLE',
                             role_id=self.role,
                             label=ROLE_LABELS[self.role]))
        if self.figure:
            self.add_cmd(Cmd('SET_FIGURE',
                             **self.figure.to_cmd_dict()))

    def set_role(self, role):
        self.role = role
        self.add_cmd(Cmd('SET_ROLE',
                         role_id=role,
                         label=ROLE_LABELS[role]))

    def set_figure(self, figure):
        self.figure = figure
        self.add_cmd(Cmd('SET_FIGURE', **figure.to_cmd_dict()))

    def set_cards(self, cards):
        self.cards.append(cards)
        for card in cards:
            self.add_cmd(Cmd('SET_CARD', **card.to_cmd_dict()))


class UserList(object):
    def __init__(self):
        self.users = {}

    def add_user(self, pk, **kwargs):
        logging.info('[-] [NEW USER] %s' % pk)
        if pk in self.users:
            raise "User PK exists!"
        user = User(pk, **kwargs)
        self.users[pk] = user
        return user

    def get_user(self, pk):
        return self.users.get(pk, None)

    def has_user(self, pk):
        return pk in self.users

    def broadcast_cmd(self, cmd, except_user=[]):
        for pk in self.users:
            if pk in except_user:
                continue
            self.users[pk].add_cmd(cmd)


global_users = UserList()
