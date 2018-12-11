import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from app import create_app, db
from app.models import User, Role, Permission, Post,Comment

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(db=db, User=User, Role=Role, Post=Post,Comment=Comment)


manager.add_command("shell", Shell(make_context=make_shell_context))  # add command line,"shell"
manager.add_command("db", MigrateCommand)  # add command line,"db"


@manager.command  # the usage for the flask-script
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'hard to guess'
    #	app.run()
    manager.run()
