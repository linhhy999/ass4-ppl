import sys,os
from shutil import copyfile, rmtree

import platform
import subprocess
import unittest
from antlr4 import *
import shutil

ANTLR_JAR = os.environ.get('ANTLR_JAR')
TARGET = '../target/main/mc/parser' if os.name == 'posix' else os.path.normpath('../target/')
locpath = ['test','./main/mc/parser/','./main/mc/astgen/','./main/mc/utils/','./main/mc/checker','./main/mc/codegen']
for p in locpath:
    if not p in sys.path:
        sys.path.append(p)
def main(argv):
    global ANTLR_JAR, TARGET
    if len(argv) < 1:
        printUsage()
    elif argv[0] == 'gen':
        a = ["java","-jar",ANTLR_JAR,"-o","../target","-no-listener","-visitor","main/mc/parser/MC.g4"]
        print(" ".join(a))
        subprocess.run(" ".join(a))
    elif argv[0] == 'clean':
        subprocess.run(["rm","-rf","../target/main"])
    elif argv[0] == 'test':
        if os.path.isdir(TARGET) and not TARGET in sys.path:
            sys.path.append(TARGET)
        if len(argv) < 2:
            printUsage()
        elif argv[1] == 'LexerSuite':
            from LexerSuite import LexerSuite
            suite = unittest.makeSuite(LexerSuite)
            test(suite)
        elif argv[1] == 'ParserSuite':
            from ParserSuite import ParserSuite
            suite = unittest.makeSuite(ParserSuite)
            test(suite)
        elif argv[1] == 'ASTGenSuite':
            from ASTGenSuite import ASTGenSuite
            suite = unittest.makeSuite(ASTGenSuite)
            test(suite)
        elif argv[1] == 'CheckSuite':
            from CheckSuite import CheckSuite
            suite = unittest.makeSuite(CheckSuite)
            test(suite)
        elif argv[1] == 'CodeGenSuite':
            if not os.path.exists("test/solutions"):
                os.makedirs("test/solutions")
            from CodeGenSuite import CheckCodeGenSuite
            suite = unittest.makeSuite(CheckCodeGenSuite)
            test(suite)
            for i in list(os.walk("test/solutions"))[0][1]:
                file = "test/solutions/"+str(i)+"/MCClass.j"
                if os.path.isfile(file):
                    copyfile(file, "test/solutions/"+str(i)+".j")
                rmtree("test/solutions/"+str(i))
        else:
            printUsage()
    else:
        printUsage()
    

def test(suite):
    from pprint import pprint
    from io import StringIO
    stream = StringIO()
    runner = unittest.TextTestRunner(stream=stream)
    result = runner.run(suite)
    print('Tests run ', result.testsRun)
    print('Errors ', result.errors)
    pprint(result.failures)
    stream.seek(0)
    print('Test output\n', stream.read())

def printUsage():
    print("python3 run.py gen")
    print("python3 run.py test LexerSuite")
    print("python3 run.py test ParserSuite")
    print("python3 run.py test ASTGenSuite")
    print("python3 run.py test CheckSuite")
    print("python3 run.py test CodeGenSuite")

if __name__ == "__main__":
   main(sys.argv[1:])
