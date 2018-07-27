from flask import Flask, render_template, render_template_string
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee

app = Flask(__name__)

# Has to be here as it requires app and is required in database creation.
import config

db = SQLAlchemy(app)
engine = create_engine(app.config['DATABASE_PATH'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
whooshee = Whooshee(app)

# Load order is important here, otherwise commands dont have access to all the models.
from models import *
from commands import initdb, rmdb, reinitdb, testdata, testsearch, reindex
from helpers import ListConverter

app.url_map.converters['list'] = ListConverter


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/search/<list:query>/<list:filters>', methods=['post', 'get'])
def search(query: str, filters: list):
    results = {}
    if 'all' in filters or 'doctors' in filters:
        results['doctors'] = []
        for obj in Doctor.search(query=query).all():
            results['doctors'].append(obj)
    print(Doctor.search(['test']).__class__)
    if 'all' in filters or 'organisations' in filters:
        results['organisations'] = []
        for obj in Organisation.search(query=query).all():
            results['organisations'].append(obj)
    if 'all' in filters or 'resources' in filters:
        results['resources'] = []
        pass
    if 'all' in filters or 'guides' in filters:
        results['guides'] = []
        for obj in Guide.search(query=query).all():
            results['guides'].append(obj)
    if 'all' in filters or 'users' in filters:
        results['users'] = []
        for obj in User.search(query=query).all():
            results['users'].append(obj)

    return render_template('search.html', results=results, filters=filters, query=query)


@app.route('/doctors/')
def doctors():
    dlist = Doctor.query.all()
    return render_template('doctors.html', doctors=dlist)


@app.route('/doctor/<uuid_id>')
def doctor(uuid_id):
    doctor_object = Doctor.query.filter(Doctor.id == uuid_id).first()
    ratings = doctor_object.get_ratings()
    rl = {}
    for r in ratings:
        if r.category not in rl.keys():
            rl[r.category] = {'num': 0, 'total': 0, 'avg': 0, 'category_name': r.name}
        rl[r.category]['num'] += 1
        rl[r.category]['total'] += r.rating
    for key, value in rl.items():
        value['avg'] = round(value['total'] / value['num'], 1)
    return render_template('doctor.html', doctor=doctor_object, ratings=rl)


@app.route('/organisations/')
def organisations():
    organisations = Organisation.query.all()
    return render_template('organisations.html', organisations=organisations)


@app.route('/organisation/<uuid_id>')
def organisation(uuid_id):
    org = Organisation.query.filter(Organisation.id == uuid_id).first()
    employees = Doctor.query.filter(Doctor.organisation_id == uuid_id).all()
    return render_template('organisation.html', organisation=org, employees=employees)


def todo():
    return render_template_string('Todo')


@app.route('/resources/')
def resources():
    return todo()


@app.route('/resource/<uuid>')
def resource(uuid):
    return todo()


@app.route('/guides/')
def guides():
    guides = Guide.query.all()
    return render_template('guides.html', guides=guides)


@app.route('/guide/<uuid>')
def guide(uuid):
    print(uuid)
    guide = Guide.query.filter(Guide.id == str(uuid)).first()
    return render_template('guide.html', guide=guide)

@app.route('/user/<uuid>')
def user(uuid):
    return todo()


@app.route('/contact/')
def contact():
    return todo()

if __name__ == '__main__':
    app.run()
