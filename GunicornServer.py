# import os
# import sys
# from gunicorn.app.base import Application

# from manage import create_app, db
# from flask_migrate import Migrate, MigrateCommand
# from flask_script import Manager
# from flask_script import Command, Option


# class GunicornServer(Command):
#     description = 'to run the app within Gunicorn'


# def __init__(self, host='0.0.0.0', port=5000, workers=2):
#     self.port = port
#     self.host = host
#     self.workers = workers


# def get_options(self):
#     return (
#         Option('-H', '--host',
#                dest='host',
#                default=self.host),

#         Option('-p', '--port',
#                dest='port',
#                type=int,
#                default=self.port),

#         Option('-w', '--workers',
#                dest='workers',
#                type=int,
#                default=self.workers),
#     )


# def handle(self, app, host, port, workers):

#     from gunicorn import version_info
#     if version_info < (0, 9, 0):
#         from gunicorn.arbiter import Arbiter
#         from gunicorn.config import Config
#         arbiter = Arbiter(
#             Config(
#                 {'bind': "%s:%d" % (host, int(port)), 'workers': workers}
#             ),
#             app
#         )
#         arbiter.run()
#     else:
#         from gunicorn.app.base import Application

#         class FlaskApplication(Application):
#             def init(self, parser, opts, args):
#                 return {
#                     'bind': '{0}:{1}'.format(host, port),
#                     'workers': workers
#                 }

#             def load(self):
#                 return app

#         FlaskApplication().run()


# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# manager = Manager(app)
# # Adding gunicorn based runserver command
# manager.add_command("gunicorn", GunicornServer())
