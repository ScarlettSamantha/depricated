import faker
import urllib3
from TransHelp import app, db
from models import Doctor, Address, Organisation, OrganisationAddress, RatingCategory, Rating, \
    Specialisation, DoctorSpecialisation, Tag, ObjectTag, User, Guide
from models.rating import RateAbleObjects
from models.objectTag import TaggableObjects
from random import randint
from flask_whooshee import Whooshee
from os.path import exists, dirname, getctime
from os import makedirs
from time import time
from random import randrange
from math import ceil

@app.cli.command()
def reindex() -> None:
    whooshee = Whooshee(app)
    whooshee.reindex()

@app.cli.command()
def testsearch() -> None:
    query = Doctor.query.whooshee_search('Courtney')
    print(query.count())
    for x in query.all():
        print(x.name)

def get_md_cache(fetch_if_missing:bool=True, path:str='./tmp/md_cache.md') -> str:
    if not exists(dirname(path)):
        makedirs(dirname(path))
    # Cache Timeout is 1 month
    if not exists(path) or (getctime(path) + (3600 * 24 * 30)) < time():
        print('Markdown data cache does not exists or is out of data, fetching new cache.')
        url = 'https://gist.githubusercontent.com/rt2zz/e0a1d6ab2682d2c47746950b84c0b6ee/raw/83b8b4814c3417111b9b9bef86a552608506603e/markdown-sample.md'
        md_test_data = urllib3.PoolManager().request('GET', url).data.decode()
        fp = open(path, 'w+')
        fp.truncate(0)
        fp.seek(0)
        fp.write(md_test_data)
        fp.flush()
        fp.close()
    else:
        print('Found markdown cache valid for %s days' % round(((((getctime(path) + (3600 * 24 * 30)) - time()) / 3600) / 24), 2))
    fp = open(path, 'r')
    cache_data = fp.read()
    fp.close()
    return cache_data


@app.cli.command()
def testdata() -> None:
    f = faker.Faker()
    al, dl, ol, rcl, rl, dsl, tl, unamel, ul = [], [], [], [], [], [], [], [], []

    for _ in range(500):
        uname = f.user_name()
        if uname in unamel:
            continue
        u = User(username=uname, password=f.ipv6(), prefix=f.prefix(), name=f.name(), suffix=f.suffix(),
                 email=str(randrange(1, 99)) + f.email(), use_username=True if randrange(0,2) != 1 else False)
        ul.append(u)
        unamel.append(uname)
        db.session.add(u)
    db.session.commit()
    md_test_data= get_md_cache()
    for _ in range(60):
        g = Guide(title=f.text(max_nb_chars=10), content=md_test_data, _author_id=ul[randint(0, ul.__len__() - 1)].id)
        db.session.add(g)

    for _ in range(60):
        o = Organisation(name=f.company(), phone=f.phone_number(), website=f.url(), email=str(randrange(1, 99)) + f.email())
        ol.append(o)
        db.session.add(o)

    db.session.commit()

    for _ in range(300):
        a = Address(city=f.city(), country=f.country_code(), postcode=f.postcode(), line1=f.street_name(),
                    line2=f.building_number(),
                    province=f.state())
        d = Doctor(name=f.name(), email=str(randint(1, 99)) + f.email(), website=f.url(), phone=f.phone_number(), prefix=f.prefix(),
                   suffix=f.suffix(),
                   organisation_id=ol[randint(0, ol.__len__() - 1)].id,
                   note=f.text(max_nb_chars=randint(50, 200)),
                   is_blocked=True if randint(1, 2) == 1 else False,
                   is_trans_friendly=True if randint(10, 50) < 40 else False,
                   has_warning=True if randint(1, 20) == 1 else False)
        if d.has_warning:
            d.warning_note = f.text(max_nb_chars=randint(50, 200))
        t = Tag(name=f.sentence(nb_words=randint(1, 2), variable_nb_words=True))
        al.append(a)
        dl.append(d)
        tl.append(t)
        db.session.add(a)
        db.session.add(d)
        db.session.add(t)

    db.session.commit()

    for o_obj in ol:
        oa = OrganisationAddress(organisation_id=o_obj.id, address_id=al[randint(0, al.__len__() - 1)].id)
        db.session.add(oa)

    for _ in range(10):
        rc = RatingCategory(name=f.sentence(nb_words=3, variable_nb_words=True))
        name = f.sentence(nb_words=2, variable_nb_words=True)
        if name[-1] == '.':
            name = name[:-1]
        ds = Specialisation(name=name)
        rcl.append(rc)
        dsl.append(ds)
        db.session.add(rc)
        db.session.add(ds)

    db.session.commit()

    for oo in ol:
        for _ in range(5, 10):
            obt = ObjectTag(object_type=TaggableObjects.organisation, object_id=oo.id,
                            tag_id=tl[randint(0, tl.__len__() - 1)].id)
            db.session.add(obt)
        for _ in range(5, 45):
            r = Rating(object_type=RateAbleObjects.organisation, object_id=oo.id, rating=randint(1, 100),
                       category=rcl[randint(0, rcl.__len__() - 1)].id)
        rl.append(r)
        db.session.add(r)

    for do in dl:
        for _ in range(5, 10):
            obt = ObjectTag(object_type=TaggableObjects.doctor, object_id=do.id,
                            tag_id=tl[randint(0, tl.__len__() - 1)].id)
            db.session.add(obt)
        for _ in range(1, 5):
            ds = DoctorSpecialisation(doctor_id=do.id, specialisation_id=dsl[randint(0, dsl.__len__() - 1)].id)
            db.session.add(ds)
        for _ in range(15, 45):
            r = Rating(object_type=RateAbleObjects.doctor, object_id=do.id, rating=randint(1, 100),
                       category=rcl[randint(0, rcl.__len__() - 1)].id)
            rl.append(r)
            db.session.add(r)
    db.session.commit()
