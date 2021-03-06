from unittest import TestCase
from sys import version_info

from inirama import Namespace, InterpolationNamespace


class MainTest(TestCase):

    def test_parse(self):
        parser = Namespace(prekey='prevalue')
        parser.read('test.ini')
        parser.read('tests/test.ini', 'tests/invalid.ini', 'tests/append.ini')

        self.assertTrue(parser['main'])
        self.assertTrue(parser['main']['key'])
        self.assertTrue(parser['main']['additional'])
        self.assertEqual(parser['DEFAULT']['prekey'], 'prevalue')
        self.assertEqual(parser['DEFAULT']['defkey'], 'defvalue')
        self.assertEqual(parser['other']['foo'], 'bar/zeta')
        self.assertEqual(parser['other']['long'], 'long value')
        self.assertEqual(parser['other']['continuation'], 'one\ntwo\nthree')
        self.assertEqual(parser['other']['safe_value'], 'c:\\\\test\\')
        self.assertEqual(parser['other']['b'], '[test]')
        self.assertEqual(parser['other']['number'], 123)
        self.assertEqual(parser['other']['key-with-hyphen'], 'yes')
        self.assertEqual(parser['other']['dot.name'], 'yes')
        self.assertEqual(parser['other']['WRONG_case'], 'yes')

        self.assertTrue('other' in parser)
        self.assertFalse('another' in parser)

        parser['main']['test'] = 123
        self.assertEqual(parser['main']['test'], 123)

        parser['main']['test'] = '1223a'
        self.assertEqual(parser['main']['test'], '1223a')

    def test_interpolation(self):
        parser = InterpolationNamespace()
        parser.default_section = 'main'
        parser.read('tests/vars.ini')
        self.assertEqual(parser['main']['var_test'], 'Hello world!')
        self.assertEqual(dict(parser['main'].items(raw=True))['var_test'], 'Hello { test}!')

        parser['main']['foo'] = 'bar {var_test}'
        self.assertEqual(parser['main']['foo'], 'bar Hello world!')

        parser['main']['test'] = '{foo}'
        if version_info >= (2, 7):
            with self.assertRaises(ValueError):
                self.assertEqual(parser['main']['foo'], 'bar Hello world!')

        parser['main']['test'] = 'parse {unknown}done'
        self.assertEqual(parser['main']['test'], 'parse done')
        self.assertEqual(parser['other']['b'], 'Hello parse done! start')

        test = dict(parser.default.items())
        self.assertTrue('parse' in test['foo'])

    def test_write(self):
        from tempfile import mkstemp

        _, target = mkstemp()

        parser = Namespace()
        parser.read('tests/vars.ini')
        parser.write(target)

        with open(target) as f:
            source = f.read()
            self.assertTrue('[main]' in source)

    def test_default(self):
        parser = Namespace()
        parser.default_section = 'main'
        parser.read('tests/test.ini')
        parser.read('tests/default.ini', update=False)

        self.assertEqual(parser['main']['key'], 'value')
        self.assertEqual(parser['main']['newkey'], 'default')
