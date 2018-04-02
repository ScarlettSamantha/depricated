import glob
from os.path import dirname, exists, isfile
from os import makedirs, unlink
from markdown import Markdown
from .markdown.images import FlaskStaticImageExtension
from TransHelp import app, db
from models.guide import Guide


def _preparse(data: str) -> str:
    return data


def _compile_markdown(md: str):
    markdown = Markdown(output_format='html5', safe_mode='escape', extensions=['markdown.extensions.extra',
                                                                               'markdown.extensions.nl2br',
                                                                               'markdown.extensions.footnotes',
                                                                               'markdown.extensions.sane_lists',
                                                                               'markdown.extensions.smarty',
                                                                               'markdown.extensions.toc',
                                                                               FlaskStaticImageExtension()])
    return markdown.convert(md)


def cache_pattern():
    return app.config['GUIDE_CACHE_FILE_PATTERN']


def cache_folder():
    return dirname(app.config['GUIDE_CACHE_FILE_PATTERN'])


def clear_cache():
    if not exists(cache_folder()):
        return
    for f in glob.glob((cache_pattern() % '*')):
        if not isfile(f):
            continue
        unlink(f)


def get_cache_file(id: str):
    return cache_pattern() % id


def compile(guide: Guide):
    if not exists(cache_folder()):
        makedirs(cache_folder(), exist_ok=True)
    to = cache_pattern() % guide.id
    if type(guide) == type(str):
        guide = Guide.query.find(Guide.id == guide).first()
        if guide is None:
            return False
    result = str(guide.content)
    result = _preparse(result)
    result = _compile_markdown(result)
    fp = open(to, 'w+')
    fp.truncate(0)
    fp.seek(0)
    fp.write(result)
    fp.flush()
    fp.close()
    guide.set_cache(to)
    return True


def compile_all():
    for g in Guide.query.all():
        compile(g)
        db.session.add(g)
    db.session.commit()


def compile_needed():
    for g in Guide.needs_recompilation():
        compile(g)
        db.session.add(g)
    db.session.commit()
