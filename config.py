from flask import request
from TransHelp import app
from os.path import join, dirname

app.config['SERVER_NAME'] = '127.0.0.1:5000'
app.config['DOCUMENT_ROOT'] = dirname(__file__)
app.config['DATABASE_PATH'] = 'sqlite:///' + join(app.config['DOCUMENT_ROOT'], './test.db')
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_PATH']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_METHOD'] = 'pbkdf2:sha512'
app.config['SECURITY_PASSWORD_SALT_LENGTH'] = 10

app.config['GUIDE_CACHE_FILE_EXTENSION'] = 'html'
app.config['GUIDE_CACHE_FILE_PATTERN'] = join(app.config['DOCUMENT_ROOT'], 'tmp/_guides_cache/%s.'
                                              + app.config['GUIDE_CACHE_FILE_EXTENSION'])

app.config['WHOOSH_BASE'] = join(app.config['DOCUMENT_ROOT'], 'search.db')