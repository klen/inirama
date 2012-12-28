"""
    Parse INI files.

"""

__version__ = '0.1.0'
__project__ = 'Inirama'
__author__ = "Kirill Klenov <horneds@gmail.com>"
__license__ = "BSD"


import re
from collections import OrderedDict


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
        self.source = re.sub(r'\\\n\s*', '', self.source)


undefined = object()


class Section(dict):

    depth = 10

    @property
    def context(self):
        return dict(iter(self))

    def __setitem__(self, name, value):
        super(Section, self).__setitem__(name, str(value))

    def __getitem__(self, name):
        value = super(Section, self).__getitem__(name)
        sample = undefined
        cnt = 0
        while sample != value:
            if cnt > self.depth:
                raise ValueError("Reached maximum depth of interpretation by key: {0}".format(name))
            sample, value, cnt = value, value.format(**self), cnt + 1
        return value

    def __iter__(self):
        for key in super(Section, self).keys():
            yield key, self[key]


class Namespace:

    default_section = 'default'
    silent_read = True
    section_type = Section

    def __init__(self, **default_items):
        self.sections = OrderedDict()
        if default_items:
            self[self.default_section] = self.section_type(**default_items)

    def read(self, *files):
        """ Read and parse INI files.
        """
        for f in files:
            try:
                with open(f, 'r') as ff:
                    self.parse(ff.read())
            except (IOError, TypeError, SyntaxError):
                if not self.silent_read:
                    raise

    def write(self, f):
        if isinstance(f, str):
            f = open(f, 'w')

        if not isinstance(f, file):
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

            if token[0] == 'SECTION':
                section = token[1].strip('[]')

    def __getitem__(self, name):
        """ Look name in self sections.
        """
        if not name in self.sections:
            self.sections[name] = self.section_type()
        return self.sections[name]
