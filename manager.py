from flask_script import Manager
from app import app, db
from app.models import User
import unittest

manager = Manager(app)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)


@manager.command
def create_db():
    db.create_all()


@manager.command
def drop_db():
    db.drop_all()


@manager.command
def test():
    """ Runs the unit test without test coverage"""
    tests = unittest.TestLoader().discover('tests',  pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()

