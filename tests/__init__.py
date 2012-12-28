from unittest import TestCase

from inirama import Namespace


class MainTest(TestCase):

    def test_parse(self):
        parser = Namespace()
        parser.read('test.ini')
        parser.read('tests/test.ini', 'tests/invalid.ini', 'tests/append.ini')

        self.assertTrue(parser['main'])
        self.assertTrue(parser['main']['key'])
        self.assertTrue(parser['main']['additional'])
        self.assertEqual(parser['default']['defkey'], 'defvalue')
        self.assertEqual(parser['other']['foo'], 'bar/zeta')
        self.assertEqual(parser['other']['long'], 'long value')

        parser['main']['test'] = 123
        self.assertEqual(parser['main']['test'], '123')

    def test_evalate(self):
        parser = Namespace()
        parser.read('tests/vars.ini')
        self.assertEqual(parser['main']['var_test'], 'Hello world!')

        parser['main']['foo'] = 'bar {var_test}'
        self.assertEqual(parser['main']['foo'], 'bar Hello world!')

        self.assertEqual(parser['main'].context, {'foo': 'bar Hello world!', 'test': 'world', 'var_test': 'Hello world!'})

        parser['main']['test'] = '{foo}'
        with self.assertRaises(KeyError):
            self.assertEqual(parser['main']['foo'], 'bar Hello world!')

    def test_write(self):
        from tempfile import mkstemp

        _, target = mkstemp()

        parser = Namespace()
        parser.read('tests/vars.ini')
        parser.write(target)

        with open(target) as f:
            source = f.read()
            self.assertTrue('[main]' in source)
