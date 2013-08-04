# -*- coding: UTF-8 -*-

import logging
import tornado.escape
import tornado.auth
import tornado.web

from sgs.user import global_users
from sgs.game import global_game
from sgs.cmd import Cmd


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None
        return tornado.escape.json_decode(user_json)


class AuthLoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        name = self.get_argument("name")
        user_dict = {'pk': name, 'name': name}
        if global_users.has_user(name):
            # TODO: 恢复用户状态
            self.redirect("/auth/login")
        else:
            global_users.add_user(**user_dict)
        self.set_secure_cookie("user", tornado.escape.json_encode(user_dict))
        self.redirect("/")


#class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
#    @tornado.web.asynchronous
#    @gen.coroutine
#    def get(self):
#        if self.get_argument("openid.mode", None):
#            user = yield self.get_authenticated_user()
#            user_dict = tornado.escape.json_encode(user)
#            self.set_secure_cookie("sgs_user", user_dict)
#            self.redirect("/")
#            return
#        self.authenticate_redirect(ax_attrs=["name"])


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.write("You are now logged out")


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if not self.current_user\
           or not global_users.has_user(self.current_user['pk']):
            self.redirect('/auth/login')
        else:
            self.render("game.html")


class SgsCmdRequestHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        cmd_args = self.request.arguments
        cmd_args.pop('_xsrf', None)
        cmd = cmd_args.pop('cmd')[0]
        cmd_args = dict([(k, v[0]) if len(v) == 1 else v
                         for k, v in cmd_args.iteritems()])
        user = global_users.get_user(self.current_user['pk'])
        if user.seat_id is not None and 'seat_id' not in cmd_args:
            cmd_args['seat_id'] = user.seat_id
        cmd = Cmd(cmd, sender=user.pk, **cmd_args)
        logging.info('<-- [%s] %s' % (cmd, cmd_args))
        self.write(dict(cmds=[cmd.get_ack_cmd().to_simple_dict()]))
        global_game.handle_cmd(cmd)
        #global_users.broadcast_cmd(cmd)

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        user_dict = self.get_current_user()
        user = global_users.get_user(user_dict['pk'])
        if user:
            user.get_cmds(self.on_new_cmd)
        else:
            self.write(dict(cmds=[]))

    def on_new_cmd(self, cmds):
        # Closed client connection
        if self.request.connection.stream.closed():
            user = global_users.get_user(self.get_current_user()['pk'])
            user.resend_cmd(cmds)
            return
        self.finish(dict(cmds=[cmds.to_simple_dict()]))
