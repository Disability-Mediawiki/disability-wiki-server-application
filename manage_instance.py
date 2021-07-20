import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from application import blueprint
from application.main import create_app, db
from flask_cors import CORS
from disability_core.MessageController import MessageController


app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

CORS(app, resources={r'/*': {'origins': '*'}})


app.app_context().push()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    msg = MessageController()
    msg.run()
    # app.run(port=8181, host='0.0.0.0', debug=True)
    # print('app running')


if __name__ == '__main__':
    manager.run()
