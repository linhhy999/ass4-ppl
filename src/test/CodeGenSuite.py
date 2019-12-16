import unittest
from TestUtils import TestCodeGen
from AST import *


class CheckCodeGenSuite(unittest.TestCase):
    def test_int(self):
        """Simple program: int main() {} """
        input = """void main() {
            putInt(4+5);
            4+5;
            5;
            1.2==5.2;
            putFloat(4+5.5);
        }"""
        expect = "99.5"
        self.assertTrue(TestCodeGen.test(input,expect,500))
    def test_int_ast(self):
        input = Program([
            FuncDecl(Id("main"),[],VoidType(),Block([
                CallExpr(Id("putInt"),[IntLiteral(5)])]))])
        expect = "5"
        self.assertTrue(TestCodeGen.test(input,expect,501))
    def test_inst(self):
        input = """void main() {
            putInt(4+5);
            4+5;
            5;
            putFloat(4+5.5);
            if (3 == 4) {
                5 == 4;
                4+5;
                5;
                1.2==5.2;
            }
            else {
                putString("Nam");
            }
        }"""
        expect = "99.5Nam"
        self.assertTrue(TestCodeGen.test(input,expect,502))
