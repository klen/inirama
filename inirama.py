"""
    Parse INI files.

"""
from __future__ import unicode_literals, print_function

import re

import io
from collections import OrderedDict


__version__ = '0.2.3'
__project__ = 'Inirama'
__author__ = "Kirill Klenov <horneds@gmail.com>"
__license__ = "BSD"


class Scanner(object):

    def __init__(self, source, ignore=None, patterns=None):
        """ Init Scanner instance.

            :param patterns: List of token patterns [(token, regexp)]
            :param ignore: List of ignored tokens
        """
        self.reset(source)
        if patterns:
            self.patterns = []
            for k, r in patterns:
                self.patterns.append((k, re.compile(r)))

        if ignore:
            self.ignore = ignore

    def reset(self, source):
        """ Reset scanner.

            :param source: Source for parsing
        """
        self.tokens = []
        self.source = source
        self.pos = 0

    def scan(self):
        """ Scan source and grab tokens.
        """
        self.pre_scan()

        token = None
        end = len(self.source)

        while self.pos < end:

            best_pat = None
            best_pat_len = 0

            # Check patterns
            for p, regexp in self.patterns:
                m = regexp.match(self.source, self.pos)
                if m:
                    best_pat = p
                    best_pat_len = len(m.group(0))
                    break

            if best_pat is None:
                raise SyntaxError("SyntaxError[@char {0}: {1}]".format(self.pos, "Bad token."))

            # Ignore patterns
            if best_pat in self.ignore:
                self.pos += best_pat_len
                continue

            # Create token
            token = (
                best_pat,
                self.source[self.pos:self.pos + best_pat_len],
                self.pos,
                self.pos + best_pat_len,
            )

            self.pos = token[-1]
            self.tokens.append(token)

    def pre_scan(self):
        """ Prepare source.
        """
        pass

    def __repr__(self):
        """ Print the last 5 tokens that have been scanned in
        """
        return 'Scanner: ' + ','.join("{0}({2}:{3})".format(*t) for t in self.tokens[-5:])


class INIScanner(Scanner):
    patterns = [
        ('SECTION', re.compile(r'\[\w+\]')),
        ('IGNORE', re.compile(r'[ \r\t\n]+')),
        ('COMMENT', re.compile(r'[;#].*')),
        ('KEY', re.compile(r'[\w_]+\s*[:=].*'))]

    ignore = ['IGNORE']

    def pre_scan(self):
        escape_re = re.compile(r'\\\n[\t ]+')
        self.source = escape_re.sub('', self.source)


undefined = object()


class Section(dict):

    @property
    def context(self):
        return self

    def __init__(self, namespace, *args, **kwargs):
        super(Section, self).__init__(*args, **kwargs)
        self.namespace = namespace

    def __setitem__(self, name, value):
        super(Section, self).__setitem__(name, str(value))

    def __iter__(self):
        for key in super(Section, self).keys():
            yield key, self[key]


class InterpolationSection(Section):

    var_re = re.compile('{([^}]+)}')

    @property
    def context(self):
        return dict(iter(self))

    def get(self, name, default=None):
        if name in self:
            return self[name]
        return default

    def __interpolate__(self, math):
        try:
            # return self[math.group(1)]
            key = math.group(1)
            return self.namespace.default.get(key) or self[key]
        except KeyError:
            return ''

    def __getitem__(self, name):
        value = super(InterpolationSection, self).__getitem__(name)
        sample = undefined
        while sample != value:
            try:
                sample, value = value, self.var_re.sub(self.__interpolate__, value)
            except RuntimeError:
                raise ValueError("Interpolation failed: {0}".format(name))
        return value


class Namespace(object):

    default_section = 'DEFAULT'
    silent_read = True
    section_type = Section

    def __init__(self, **default_items):
        self.sections = OrderedDict()
        for k, v in default_items.items():
            self[self.default_section][k] = v

    @property
    def default(self):
        """ Return default section or empty dict.
        """
        return self.sections.get(self.default_section, dict())

    def read(self, *files):
        """ Read and parse INI files.
        """
        for f in files:
            try:
                with io.open(f, encoding='utf-8') as ff:
                    self.parse(ff.read())
            except (IOError, TypeError, SyntaxError, io.UnsupportedOperation):
                if not self.silent_read:
                    raise

    def write(self, f):
        """
            Write self as INI file.

            :param f: File object or path to file.
        """
        if isinstance(f, str):
            f = io.open(f, 'w', encoding='utf-8')

        if not hasattr(f, 'read'):
            raise AttributeError("Wrong type of file: {0}".format(type(f)))

        for section in self.sections.keys():
            f.write('[{0}]\n'.format(section))
            for k, v in iter(self[section]):
                f.write('{0:15}= {1}\n'.format(k, v))
            f.write('\n')
        f.close()

    def parse(self, source):
        """ Parse INI source.
        """
        scanner = INIScanner(source)
        scanner.scan()

        section = self.default_section

        for token in scanner.tokens:
            if token[0] == 'KEY':
                name, value = re.split('[=:]', token[1], 1)
                self[section][name.strip()] = value.strip()

            elif token[0] == 'SECTION':
                section = token[1].strip('[]')

    def __getitem__(self, name):
        """ Look name in self sections.
        """
        if not name in self.sections:
            self.sections[name] = self.section_type(self)
        return self.sections[name]

    def __repr__(self):
        return "<Namespace: {0}>".format(self.sections)


class InterpolationNamespace(Namespace):

    section_type = InterpolationSection
