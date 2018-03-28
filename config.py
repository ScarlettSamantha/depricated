from TransHelp import app
from os.path import join, dirname

db_path = 'sqlite:///' + join(dirname(__file__), './test.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
