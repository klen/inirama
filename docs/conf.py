# -*- coding: utf-8 -*-
import os
import sys
import datetime

from inirama import __version__ as release

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'inirama'
copyright = u'%s, Kirill Klenov' % datetime.datetime.now().year
version = '.'.join(release.split('.')[:2])
exclude_patterns = ['_build']
html_use_modindex = False
html_show_sphinx = False
htmlhelp_basename = 'Iniramadoc'
latex_documents = [
    ('index', 'Inirama.tex', u'Inirama Documentation',
        u'Kirill Klenov', 'manual'),
]
latex_use_modindex = False
latex_use_parts = True
man_pages = [
    ('index', 'inirama', u'Inirama Documentation',
     [u'Kirill Klenov'], 1)
]
pygments_style = 'tango'
html_theme = 'default'
html_theme_options = {}

# lint_ignore=W0622
