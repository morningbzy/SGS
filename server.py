
import tornado.ioloop
import tornado.web
import os.path

from tornado.options import define, options, parse_command_line

from sgs.cmd_handlers import IndexHandler, SgsCmdRequestHandler
from sgs.cmd_handlers import AuthLoginHandler, AuthLogoutHandler


define("port", default=8888, help="run on the given port", type=int)


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", IndexHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
            (r"/sgs/cmd", SgsCmdRequestHandler),
        ],
        cookie_secret="123",
        login_url="/auth/login",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=True
    )
    app.listen(options.port)
    print 'Listening @ %s ...' % options.port
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
