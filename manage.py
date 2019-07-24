import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gsauxupdtlrdxw:570b63e6418005cb3a9df34e84edf0044136a57b1b3705847d29a33415ff734c@ec2-54-243-208-234.compute-1.amazonaws.com:5432/d2od04jmuld6tc'
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
