from typing import List
from flask_whooshee import WhoosheeQuery

class IsSearchAble:

    __MODE_AND = 0
    __MODE_OR = 1

    _is_searchable = True

    @classmethod
    def search(cls, query: List[str], mode:int = __MODE_AND) -> WhoosheeQuery:
        if mode == cls.__MODE_AND:
            query = 'and '.join(query)
        elif mode == cls.__MODE_OR:
            query = 'or '.join(query)
        result_query = cls.query.whooshee_search(query)
        return result_query