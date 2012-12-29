from unittest import TestCase

from inirama import Namespace, InterpolationNamespace


class MainTest(TestCase):

    def test_parse(self):
        parser = Namespace()
        parser.read('test.ini')
        parser.read('tests/test.ini', 'tests/invalid.ini', 'tests/append.ini')

        self.assertTrue(parser['main'])
        self.assertTrue(parser['main']['key'])
        self.assertTrue(parser['main']['additional'])
        self.assertEqual(parser['DEFAULT']['defkey'], 'defvalue')
        self.assertEqual(parser['other']['foo'], 'bar/zeta')
        self.assertEqual(parser['other']['long'], 'long value')
        self.assertEqual(parser['other']['safe_value'], 'c:\\\\test\\')
        self.assertEqual(parser['other']['b'], '[test]')

        parser['main']['test'] = 123
        self.assertEqual(parser['main']['test'], '123')

    def test_interpolation(self):
        parser = InterpolationNamespace()
        parser.default_section = 'main'
        parser.read('tests/vars.ini')
        self.assertEqual(parser['main']['var_test'], 'Hello world!')

        parser['main']['foo'] = 'bar {var_test}'
        self.assertEqual(parser['main']['foo'], 'bar Hello world!')

        parser['main']['test'] = '{foo}'
        with self.assertRaises(ValueError):
            self.assertEqual(parser['main']['foo'], 'bar Hello world!')

        parser['main']['test'] = 'parse {unknown}done'
        self.assertEqual(parser['main']['test'], 'parse done')
        self.assertEqual(parser['other']['b'], 'Hello parse done! start')

    def test_write(self):
        from tempfile import mkstemp

        _, target = mkstemp()

        parser = Namespace()
        parser.read('tests/vars.ini')
        parser.write(target)

        with open(target) as f:
            source = f.read()
            self.assertTrue('[main]' in source)
