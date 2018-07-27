from TransHelp import db

class IsRateAble(object):

    _ID_FIELD_ = 'id'
    _is_rateable = True

    def get_ratings(self):
        from models.rating import Rating, RateAbleObjects
        from models.ratingCategory import RatingCategory
        class_obj = RateAbleObjects(self.__class__)
        obj = db.session.query(Rating.category, Rating.rating, RatingCategory.name)\
            .join(RatingCategory, Rating.category == RatingCategory.id)\
            .filter(Rating.object_id == getattr(self, getattr(self, '_ID_FIELD_')))\
            .filter(Rating.object_type == class_obj)\
            .all()
        return obj
