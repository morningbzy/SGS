# -*- coding: UTF-8 -*-

import simplejson as json
import uuid


class Cmd(object):
    def __init__(self, cmd=None, sender='GAME', **kwargs):
        self.pk = str(uuid.uuid4())
        self.cmd = cmd
        self.sender = sender
        self.kwargs = kwargs

    def __str__(self):
        return json.dumps(self.to_simple_dict())

    def __getattr__(self, attr):
        if attr in self.kwargs:
            return self.kwargs[attr]
        else:
            return getattr(super(Cmd, self), attr)

    def to_simple_dict(self):
        data = {
            'id': self.pk,
            'cmd': self.cmd,
            'sender': self.sender,
        }
        data.update(self.kwargs)
        return data

    def update_args(self, args):
        self.kwargs.update(args)

    def get_ack_cmd(self):
        ack_prefix = 'ACK_%s'
        return Cmd(cmd=ack_prefix % self.cmd, **self.kwargs)
