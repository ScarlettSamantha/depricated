"""
Markdown extension for modifying local links to Django static links
Author: Melvin Koh

Eg:
    Markdown:
        ![profile_picture](images/my_profile_picture.png)
    Output without extension:
        <img alt="profile_picture" src="images/my_profile_picture.png" />
    Output with this extension:
        <img alt="profile_picture" src={% url_for('static',"images/my_profile_picture.png") %} />

    Options:
    1. Add Prefix before link:
        <img alt="profile_picture" src={% static "<prefix>/images/my_profile_picture.png" %} />


"""
from __future__ import absolute_import
from __future__ import unicode_literals
import flask
from TransHelp import app
import re

from markdown import Extension
from markdown.treeprocessors import Treeprocessor


class FlaskStaticImageTreeProcessor(Treeprocessor):
    """
     Finds all img tag with src attribute, add static tag for Django Template Language

     - Replace local source only
     - Allow additional prefix to link
    """

    local_source_regex = re.compile(r"(://)")

    def run(self, root):
        imgs = root.iter('img')
        for img in imgs:
            if img.get('src'): # If src attribute exists
                if not self.local_source_regex.search(img.get('src')):
                    if not self.config['prefix']:
                        url = flask.url_for('static', filename='images/' + img.get('src'), _external=True)
                        img.set('src', url)
                    else:
                        if self.config['prefix'].endswith('/'):
                            self.config['prefix'] = self.config['prefix'][:-1]
                        img.set('src', '{% url_for("static", filename="' + self.config['prefix'] + '/' + img.get('src') + '") %})')


class FlaskStaticImageExtension(Extension):
    def __init__(self, **kwargs):
        # Initialize Configurations
        self.config = {'prefix': ['', 'Empty prefix']}
        super(FlaskStaticImageExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        # Add DjangoStaticImage into Markdown instance
        md.registerExtension(self)
        extension = FlaskStaticImageTreeProcessor(md)
        extension.config = self.getConfigs()
        md.treeprocessors.add('flask_static_image_pattern', extension, '_end' )


def makeExtension(**kwargs):
    return FlaskStaticImageExtension(**kwargs)