'''
 *   @author Nguyen Hua Phung
 *   @version 1.0
 *   23/10/2015
 *   This file provides a simple version of code generator
 *
'''
from Utils import *
from StaticCheck import *
from StaticError import *
from Emitter import Emitter
from Frame import Frame
from abc import ABC, abstractmethod

e = None

class Symbol:
    def __init__(self,name,mtype,value=None):
        self.name = name
        self.mtype = mtype
        self.value = value

class CodeGenerator(Utils):
    def __init__(self):
        self.libName = "io"

    def init(self):
        return [Symbol("getInt", MType(list(), IntType()), CName(self.libName)),
                    Symbol("putInt", MType([IntType()], VoidType()), CName(self.libName)),
                    Symbol("putIntLn", MType([IntType()], VoidType()), CName(self.libName)),
                    Symbol("putFloatLn", MType([FloatType()], VoidType()), CName(self.libName))
                    ]

    def gen(self, ast, dir_):
        #ast: AST
        #dir_: String

        gl = self.init()
        gc = CodeGenVisitor(ast, gl, dir_)
        gc.visit(ast, None)

class ClassType(Type):
    def __init__(self, cname):
        #cname: String
        self.cname = cname

    def __str__(self):
        return "ClassType"

    def accept(self, v, param):
        return v.visitClassType(self, param)

class SubBody():
    def __init__(self, frame, sym):
        #frame: Frame
        #sym: List[Symbol]

        self.frame = frame
        self.sym = sym

class Access():
    def __init__(self, frame, sym, isLeft, isFirst):
        #frame: Frame
        #sym: List[Symbol]
        #isLeft: Boolean
        #isFirst: Boolean

        self.frame = frame
        self.sym = sym
        self.isLeft = isLeft
        self.isFirst = isFirst

class Val(ABC):
    pass

class Index(Val):
    def __init__(self, value):
        #value: Int

        self.value = value

class CName(Val):
    def __init__(self, value):
        #value: String

        self.value = value

class CodeGenVisitor(BaseVisitor, Utils):
    def __init__(self, astTree, env, dir_):
        #astTree: AST
        #env: List[Symbol]
        #dir_: File
        global e
        self.astTree = astTree
        self.env = env
        self.className = "MCClass"
        self.path = dir_
        e = Emitter(self.path + "/" + self.className + ".j")

    def visitProgram(self, ast, c):
        #ast: Program
        #c: Any
        global e
        e.printout(e.emitPROLOG(self.className, "java.lang.Object"))
        env = SubBody(None, self.env)
        for x in ast.decl:
            env = self.visit(x, env)
        # generate default constructor
        self.genMETHOD(FuncDecl(Id("<init>"), list(), None, Block(list())), c, Frame("<init>", VoidType))
        e.emitEPILOG()
        e = None
        return c

    def genMETHOD(self, consdecl, o, frame):
        #consdecl: FuncDecl
        #o: Any
        #frame: Frame

        isInit = consdecl.returnType is None
        isMain = consdecl.name.name == "main" and len(consdecl.param) == 0 and type(consdecl.returnType) is VoidType
        returnType = VoidType() if isInit else consdecl.returnType
        methodName = "<init>" if isInit else consdecl.name.name
        intype = [ArrayPointerType(StringType())] if isMain else list()
        mtype = MType(intype, returnType)

        e.printout(e.emitMETHOD(methodName, mtype, not isInit, frame))

        frame.enterScope(True)

        glenv = o

        # Generate code for parameter declarations
        if isInit:
            e.printout(e.emitVAR(frame.getNewIndex(), "this", ClassType(self.className), frame.getStartLabel(), frame.getEndLabel(), frame))
        if isMain:
            e.printout(e.emitVAR(frame.getNewIndex(), "args", ArrayPointerType(StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))

        body = consdecl.body
        e.printout(e.emitLABEL(frame.getStartLabel(), frame))

        # Generate code for statements
        if isInit:
            e.printout(e.emitREADVAR("this", ClassType(self.className), 0, frame))
            e.printout(e.emitINVOKESPECIAL(frame))
        list(map(lambda x: self.visit(x, SubBody(frame, glenv)), body.member))

        e.printout(e.emitLABEL(frame.getEndLabel(), frame))
        if type(returnType) is VoidType:
            e.printout(e.emitRETURN(VoidType(), frame))
        e.printout(e.emitENDMETHOD(frame))
        frame.exitScope();

    def visitFuncDecl(self, ast, o):
        #ast: FuncDecl
        #o: Any
        subctxt = o
        frame = Frame(ast.name, ast.returnType)
        self.genMETHOD(ast, subctxt.sym, frame)
        return SubBody(None, [Symbol(ast.name, MType(list(), ast.returnType), CName(self.className))] + subctxt.sym)

    def visitCallExpr(self, ast, o):
        #ast: CallExpr
        #o: Any
        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        sym = self.lookup(ast.method.name, nenv, lambda x: x.name)
        cname = sym.value.value
    
        ctype = sym.mtype

        in_ = ("", list())
        for x in ast.param:
            str1, typ1 = self.visit(x, Access(frame, nenv, False, True))
            in_ = (in_[0] + str1, in_[1].append(typ1))
        e.printout(in_[0])
        e.printout(e.emitINVOKESTATIC(cname + "/" + ast.method.name, ctype, frame))

    def visitIntLiteral(self, ast, o):
        #ast: IntLiteral
        #o: Any
        ctxt = o
        frame = ctxt.frame
        return e.emitPUSHICONST(ast.value, frame), IntType()

    def visitFloatLiteral(self, ast, o):
        #ast: IntLiteral
        #o: Any
        ctxt = o
        frame = ctxt.frame
        return e.emitPUSHICONST(ast.value, frame), IntType()