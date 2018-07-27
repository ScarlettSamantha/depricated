from werkzeug.routing import BaseConverter


def format_name_parts(prefix, name, suffix):
    return '%s %s %s' % (prefix, name, suffix)

class ListConverter(BaseConverter):

    def to_python(self, value):
        return value.split(',')

    def to_url(self, values):
        return ','.join(BaseConverter.to_url(value)
                        for value in values)

