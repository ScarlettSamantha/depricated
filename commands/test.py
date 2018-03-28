import faker

from TransHelp import app, db
from models import Doctor, Address, DoctorAddress, Organisation, OrganisationAddress, RatingCategory, Rating, \
    Specialisation, DoctorSpecialisation, Tag, ObjectTag
from models.rating import RateAbleObjects
from models.objectTag import TaggableObjects
from random import randint


@app.cli.command()
def testdata():
    f = faker.Faker()
    al, dl, ol, rcl, rl, dsl, tl = [], [], [], [], [], [], []
    for _ in range(100):
        a = Address(city=f.city(), country=f.country_code(), postcode=f.postcode(), line1=f.street_name(), line2=f.building_number())
        d = Doctor(name=f.name(), email=f.email(), website=f.url(), phone=f.phone(),
                   note=f.paragraphs(nb=randint(1, 3)),
                   is_blocked=True if randint(1,2) == 1 else False,
                   is_trans_friendly=True if randint(10, 50) < 40 else False,
                   has_warning=True if randint(1, 20) == 1 else False)
        t = Tag(name=f.sentence(nb_words=randint(1, 2), variable_nb_words=True))
        al.append(a)
        dl.append(d)
        tl.append(t)
        db.session.add(a)
        db.session.add(d)
        db.session.add(t)

    db.session.commit()

    for _ in range(10):
        o = Organisation(name=f.company())
        ol.append(o)
        db.session.add(o)

    db.session.commit()

    for d_obj in dl:
        da = DoctorAddress(doctor_id=d_obj.id, address_id=al[randint(0, al.__len__() - 1)].id)
        db.session.add(da)

    for o_obj in ol:
        oa = OrganisationAddress(organisation_id=o_obj.id, address_id=al[randint(0, al.__len__() - 1)].id)
        db.session.add(oa)

    for _ in range(20):
        rc = RatingCategory(name=f.sentence(nb_words=3, variable_nb_words=True))
        ds = Specialisation(name=f.sentence(nb_words=2, variable_nb_words=True))
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
        for _ in range(5, 45):
            r = Rating(object_type=RateAbleObjects.doctor, object_id=do.id, rating=randint(1, 100),
                       category=rcl[randint(0, rcl.__len__() - 1)].id)
            rl.append(r)
            db.session.add(r)
    db.session.commit()
