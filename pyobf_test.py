import unittest
import pyobf
import sys
import re
from cStringIO import StringIO

class PyObfSpec(unittest.TestCase):
    def runCode(self, code):
        old = sys.stdout
        redirected_output = sys.stdout = StringIO()
        exec(code)
        sys.stdout = old
        return redirected_output.getvalue().strip()

    def setUp(self):
        pass

    def test_assignment(self):
        string = "print '123'\nprint '456'"
        obf = pyobf.Obfuscator(string)
        self.assertEqual(obf.simple(), "0 \\'2\\'\\n0 \\'1\\'")

    def test_indent(self):
        string = "def main():\n\tprint 'hi'"
        obf = pyobf.Obfuscator(string)
        self.assertEqual(obf.simple(), "3 2():\\n\\t1 \\'0\\'")

    def test_indent_space(self):
        string = "def main():\n    print 'hi'"
        obf = pyobf.Obfuscator(string)
        self.assertEqual(obf.simple(), "3 2():\\n\\t1 \\'0\\'")

    def test_slash_quote(self):
        string = "print \'\\\'"
        obf = pyobf.Obfuscator(string)
        self.assertEqual(obf.simple(), "0 \\'\\\\'")

    def test_build_slash_quote(self):
        string = "print \'\\\'"
        obf = pyobf.Obfuscator(string)
        self.assertEqual(self.runCode(obf.build_simple()), "\\")

    def test_build_simple(self):
        string = "print 'hello world'"
        obf = pyobf.Obfuscator(string)
        self.assertEqual(self.runCode(obf.build_simple()), "hello world")

    def test_build_word(self):
        string = 'print 1\nprint 2\nprint 3\nprint 2\nprint 1'
        obf = pyobf.Obfuscator(string)
        self.assertEqual(self.runCode(obf.build_simple()), "1\n2\n3\n2\n1")

    '''
    def test_obf(self):
        string = open("pyobf.py", "r").read()
        obf = pyobf.Obfuscator(string)
        obf_str = obf.build_simple()
        self.runCode(obf.build_simple())
        self.assertEqual(1, 1)
    '''

    def tearDown(self):
        pass

if __name__ == "__main__":
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(PyObfSpec)
    unittest.TextTestRunner(verbosity=2).run(suite)
