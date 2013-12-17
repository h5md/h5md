# -*- coding: utf-8 -*-
"""
    sphinxcontrib.mathml
    ~~~~~~~~~~~~~~~~~~~~

    Convert (La)TeX math markup into MathML via blahtexml.

    :copyright: Copyright 2011-2013 by Clemens-O. Hoppe.
    :copyright: Copyright 2007-2011 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from docutils import nodes

from sphinx.errors import SphinxError
from sphinx.ext.mathbase import setup_math as mathbase_setup

from subprocess import Popen, PIPE


class MathExtError(SphinxError):
    category = 'Math extension error'


def build_mathml(self, math):
    if hasattr(self.builder, '_mathml_warned'):
        return None, None

    blahinput = math.encode('utf-8') + '\n'

    blah_args = ['blahtexml', '--mathml']

    '''FIXME: blahtexml outputs custom XML nodes inside the mathml markup
       when an error occurs, yet still returns 0 as its exit code.
    '''
    try:
        o = Popen(['echo', blahinput], stdout=PIPE)
        p = Popen(blah_args, stdin=o.stdout, stdout=PIPE)
        blahoutput, blaherrors = p.communicate()
    except OSError:
        self.builder.warn('could not call blahtexml. make sure that is '
                          'installed as well as in PATH.')
        self.builder._mathml_warned = True

    if p.returncode != 0:
        raise MathExtError('blahtexml exited with error:\n[stderr]\n%s\n'
                           '[stdout]\n%s') % (blahoutput, blaherrors)

    #FIXME: parse the xml tree properly (also see above fixme).
    return blahoutput.replace('<blahtex>\n<mathml>\n<markup>\n',
        '<math xmlns="http://www.w3.org/1998/Math/MathML">'). \
        replace('</markup>\n</mathml>\n</blahtex>\n', '</math>') or None


def html_visit_math(self, node):
    self.body.append(self.starttag(node, 'span', '', CLASS='math'))
    self.body.append(build_mathml(self, node['latex']) + '</span>')
    raise nodes.SkipNode


def html_visit_displaymath(self, node):
    self.body.append(self.starttag(node, 'div', CLASS='math'))
    self.body.append(build_mathml(self, node['latex']))

    # coh FIXME: use proper mathml markup
    # BK: numbering copied from mathjax.py
    parts = [prt for prt in node['latex'].split('\n\n') if prt.strip()]
    for i, part in enumerate(parts):
        part = self.encode(part)
        if i == 0:
            # necessary to e.g. set the id property correctly
            if node['number']:
                self.body.append('<span class="eqno">(%s)</span>' %
                                 node['number'])

    self.body.append('</div>')
    raise nodes.SkipNode


def setup(app):
    mathbase_setup(app, (html_visit_math, None),
                        (html_visit_displaymath, None))
