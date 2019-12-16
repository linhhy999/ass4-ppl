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
from MachineCode import JasminCode
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
        return [
            Symbol("getInt",     MType([],IntType()), CName(self.libName)),
            Symbol("putInt",     MType([IntType()],VoidType()), CName(self.libName)),
            Symbol("putIntLn",   MType([IntType()],VoidType()), CName(self.libName)),
            Symbol("getFloat",   MType([],FloatType()), CName(self.libName)),
            Symbol("putFloat",   MType([FloatType()],VoidType()), CName(self.libName)),
            Symbol("putFloatLn", MType([FloatType()],VoidType()), CName(self.libName)),
            Symbol("putBool",    MType([BoolType()],VoidType()), CName(self.libName)),
            Symbol("putBoolLn",  MType([BoolType()],VoidType()), CName(self.libName)),
            Symbol("putString",  MType([StringType()],VoidType()), CName(self.libName)),
            Symbol("putStringLn",MType([StringType()],VoidType()), CName(self.libName)),
            Symbol("putLn",      MType([],VoidType()), CName(self.libName))
        ]

    def gen(self, ast, dir_):
        #ast: AST
        #dir_: String

        gl = self.init()
        gc = CodeGenVisitor(ast, gl, dir_)
        gc.visit(ast, None)

class ArrayPointerType(Type):
    def __init__(self, ctype):
        #cname: String
        self.eleType = ctype

    def __str__(self):
        return "ArrayPointerType({0})".format(str(self.eleType))

    def accept(self, v, param):
        return None

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
############# PROGRAM ###############
    def visitProgram(self, ast, c):
        #ast: Program
        #c: Any
        global e
        e.printout(e.emitPROLOG(self.className, "java.lang.Object"))
        for i in ast.decl:
            if type(i) is VarDecl: self.env += [self.visit(i, None)]
            else: self.env += [Symbol(i.name.name, MType([j.varType for j in i.param],i.returnType), CName(self.className))]

        env = SubBody(None, self.env)
        for x in ast.decl:
            env = self.visit(x, env)
        # generate default constructor
        self.genMETHOD(FuncDecl(Id("<init>"), list(), None, Block(list())), c, Frame("<init>", VoidType))
        e.emitEPILOG()
        e = None
        return c
############## DECLs ################
    def genMETHOD(self, consdecl, o, frame):
        #consdecl: FuncDecl
        #o: Any
        #frame: Frame
        global e
        isInit = consdecl.returnType is None
        isMain = consdecl.name.name == "main" and len(consdecl.param) == 0 and type(consdecl.returnType) is VoidType
        returnType = VoidType() if isInit else consdecl.returnType
        methodName = "<init>" if isInit else consdecl.name.name
        intype = [ArrayPointerType(StringType())] if isMain else list() if isInit else [i.varType for i in consdecl.param]
        mtype = MType(intype, returnType)

        e.printout(e.emitMETHOD(methodName, mtype, not isInit, frame))

        frame.enterScope(True)
        try: glenv = o[:]
        except Exception as errrrr: glenv = o

        # Generate code for parameter declarations
        if isInit:
            e.printout(e.emitVAR(frame.getNewIndex(), "this", ClassType(self.className), frame.getStartLabel(), frame.getEndLabel(), glenv))
        else:
            if isMain:
                e.printout(e.emitVAR(frame.getNewIndex(), "args", ArrayPointerType(StringType()), frame.getStartLabel(), frame.getEndLabel(), glenv))
            else:
                for i in consdecl.param:
                    index = frame.getNewIndex()
                    e.printout(e.emitVAR(index, i.variable.name, i.varType, frame.getStartLabel(),frame.getEndLabel(), glenv))
                    glenv = [Symbol(i.variable.name, i.varType, Index(index))] + glenv

        body = consdecl.body
        e.printout(e.emitLABEL(frame.getStartLabel(), frame))

        # Generate code for statements
        if isInit:
            e.printout(e.emitREADVAR("this", ClassType(self.className), 0, frame))
            e.printout(e.emitINVOKESPECIAL(frame))

        self.visit(body, SubBody(frame, glenv))

        # for i in body.member:
        #     a = self.visit(i, SubBody(frame, glenv))
        #     if isinstance(i, Expr):
        #         e.printout(a[0])

        e.printout(e.emitLABEL(frame.getEndLabel(), frame))
        if type(returnType) is VoidType: e.printout(e.emitRETURN(VoidType(), frame))
        e.printout(e.emitENDMETHOD(frame))
        frame.exitScope()

    def visitFuncDecl(self, ast, o):
        #ast: FuncDecl
        #o: Any

        subctxt = o
        frame = Frame(ast.name, ast.returnType)
        self.genMETHOD(ast, subctxt.sym, frame)
        return

    def visitVarDecl(self, ast, o):
        if type(ast.varType) is ArrayType: raise Exception("Array type variable found")
        e.printout(e.emitATTRIBUTE(ast.variable, ast.varType, True, 5))
        return Symbol(ast.variable, ast.varType, CName(self.className))
############## STMTs ################
    def visitBlock(self, ast, o):
        for i in ast.member:
            if isinstance(i, CallExpr) or (isinstance(i,BinaryOp) and i.op == "="):
                e.printout(self.visit(i, o)[0])
            else:
                self.visit(i, o)

    def visitIf(self, ast, o):
        frame = o.frame
        nenv = o.sym
        e.printout(self.visit(ast.expr, Access(frame, nenv, False, True))[0])
        if ast.elseStmt == []:
            exitLabel = frame.getNewLabel()
            e.printout(e.emitIFFALSE(exitLabel,frame))
            self.visit(ast.thenStmt, o)
            if ast.thenStmt == [] or (ast.thenStmt != [] and not(type(ast.thenStmt[-1]) is Return)):
                e.printout(e.emitGOTO(exitLabel, frame))
            e.printout(e.emitLABEL(exitLabel, frame))
        else:
            falseLabel = frame.getNewLabel()
            exitLabel = frame.getNewLabel()
            e.printout(e.emitIFFALSE(falseLabel,frame))
            self.visit(ast.thenStmt, o)
            if isinstance(ast.thenStmt, Block):
                if ast.thenStmt.member == [] or (ast.thenStmt.member != [] and not(type(ast.thenStmt.member[-1]) is Return)):
                    e.printout(e.emitGOTO(exitLabel, frame))
            e.printout(e.emitLABEL(falseLabel, frame))
            self.visit(ast.elseStmt, o)
            e.printout(e.emitLABEL(exitLabel, frame))

    def visitWhile(self, ast, o):
        frame = o.frame
        whileCondition = ""

        labelCondition = frame.getNewLabel()
        labelExit = frame.getNewLabel()
        frame.conLabel += [labelCondition]
        frame.brkLabel += [labelExit]
        exp, expT = self.visit(ast.exp, Access(frame, o.sym, False, True))
        whileCondition = e.emitLABEL(labelCondition, frame) + exp + e.emitIFFALSE(labelExit,frame)
        e.printout(whileCondition)

        for i in ast.sl: self.visit(i, o)

        e.printout(e.emitGOTO(labelCondition, frame))
        e.printout(e.emitLABEL(labelExit, frame))
        frame.conLabel = frame.conLabel[:-1]
        frame.brkLabel = frame.brkLabel[:-1]

    def visitFor(self, ast, o):
        frame = o.frame
        forInit = forCondition = forIncrement = ""
        expr1, expr1t = self.visit(ast.expr1, Access(frame, o.sym, False, True))
        id, idt = self.visit(ast.id, Access(frame, o.sym, True, True))
        if not (type(idt) is IntType or type(expr1t) is IntType): raise TypeMismatchInStatement(ast)
        forInit = expr1 + id
        e.printout(forInit)

        labelCondition = frame.getNewLabel()
        labelIncrement = frame.getNewLabel()
        labelExit = frame.getNewLabel()
        frame.conLabel += [labelIncrement]
        frame.brkLabel += [labelExit]
        expr2, expr2t = self.visit(ast.expr2, Access(frame, o.sym, False, True))
        if not(type(expr2t) is IntType): raise TypeMismatchInStatement(ast)
        forCondition = e.emitLABEL(labelCondition, frame)
        forCondition = e.emitLABEL(labelCondition, frame) + self.visit(ast.id, Access(frame, o.sym, False, True))[0] + expr2 + (e.emitIFICMPGT(labelExit,frame) if ast.up else e.emitIFICMPLT(labelExit,frame))
        e.printout(forCondition)

        for i in ast.loop: self.visit(i, o)

        forIncrement = e.emitLABEL(labelIncrement, frame) + self.visit(ast.id, Access(frame, o.sym, False, True))[0] + e.emitPUSHICONST(1,frame)
        forIncrement += e.emitADDOP('+' if ast.up else '-',IntType(),frame)
        forIncrement += self.visit(ast.id, Access(frame, o.sym, True, True))[0]
        forIncrement += e.emitGOTO(labelCondition, frame)
        e.printout(forIncrement)
        e.printout(e.emitLABEL(labelExit, frame))
        frame.conLabel = frame.conLabel[:-1]
        frame.brkLabel = frame.brkLabel[:-1]

    def visitBreak(self, ast, o):
        e.printout(e.emitGOTO(o.frame.brkLabel[-1], o.frame))

    def visitContinue(self, ast, o):
        e.printout(e.emitGOTO(o.frame.conLabel[-1], o.frame))

    def visitReturn(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        if not ast.expr:
            e.printout(e.emitRETURN(VoidType(),frame))
            return
        strExpr, typeExpr = self.visit(ast.expr,Access(frame, nenv, False, True))
        e.printout(strExpr)
        if type(frame.returnType) is FloatType and type(typeExpr) is IntType:
            e.printout(e.emitI2F(frame))
            typeExpr = frame.returnType
        e.printout(e.emitRETURN(typeExpr,frame))

    def visitWith(self, ast, o):
        a=5
        frame = o.frame
        nenv = o.sym[:]
        frame.enterScope(False)
        varDecl = ""
        for i in ast.decl:
            index = frame.getNewIndex()
            varDecl += e.emitVAR(index, i.variable.name, i.varType, frame.getStartLabel(),frame.getEndLabel(), nenv)
            nenv = [Symbol(i.variable.name, i.varType, Index(index))] + nenv
        e.printout(varDecl)
        e.printout(e.emitLABEL(frame.getStartLabel(), frame))
        for i in ast.stmt: self.visit(i,SubBody(frame,nenv))
        e.printout(e.emitLABEL(frame.getEndLabel(), frame))
        frame.exitScope()
############## EXPRs ################
    def visitBinaryOp(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        left, typeLeft = self.visit(ast.left, o)
        right, typeRight = self.visit(ast.right, o)
        if not(type(typeLeft) == type(typeRight)):
            if type(typeLeft) is IntType and type(typeRight) is FloatType:
                left += e.emitI2F(frame)
                typeLeft = FloatType()
            elif type(typeLeft) is FloatType and type(typeRight) is IntType:
                right += e.emitI2F(frame)
                typeRight = FloatType()
        if ast.op in ['+','-']: return left + right + e.emitADDOP(ast.op, typeLeft, frame), typeLeft
        elif ast.op == '*': return left + right + e.emitMULOP(ast.op, typeLeft, frame), typeLeft
        elif ast.op == '/':
            if type(typeLeft) is IntType:
                return left + right + e.emitDIV(frame), IntType()
            else: return left + right + e.emitMULOP(ast.op, typeLeft, frame), typeLeft
        elif ast.op.lower() == '%': return left + right + e.emitMOD(frame), IntType()
        elif ast.op in ['>','>=','<','<=','<>','==']: return left + right + e.emitREFOP(ast.op, typeLeft, frame), BoolType()
        elif ast.op.lower() == '&&': return left + right + e.emitANDOP(frame), BoolType()
        elif ast.op.lower() == '||': return left + right + e.emitOROP(frame), BoolType()
        elif ast.op == "=": return right + left, typeLeft
        else: raise Exception("Wrong binop: " + str(ast.op))

    def visitUnaryOp(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        body, typeBody = self.visit(ast.body, o)
        if ast.op.lower() =='not':
            return body + e.emitNOT(typeBody,frame), typeBody
        elif ast.op == '-':
            return body + e.emitNEGOP(typeBody,frame), typeBody

    def visitCallExpr(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        sym = self.lookup(ast.method.name, nenv, lambda x: x.name)
        if not sym: raise Undeclared(Function(),ast.method.name)
        cname = sym.value.value

        ctype = sym.mtype

        in_ = ""
        for i, x in enumerate(ast.param):
            str1, typ1 = self.visit(x, Access(frame, nenv, False, True))
            if type(typ1) is IntType and type(sym.mtype.partype[i]) is FloatType:
                str1 += e.emitI2F(0)
            in_ = in_ + str1
        return in_ + e.emitINVOKESTATIC(cname + "/" + sym.name, ctype, frame), sym.mtype.rettype

    def visitId(self, ast, o):
        sym = self.lookup(ast.name, o.sym, lambda x:x.name)
        if not sym: raise Undeclared(Variable(), ast.name)
        if o.isLeft:
            if type(sym.value) is CName: return e.emitPUTSTATIC(sym.value.value + '/' + sym.name, sym.mtype, o.frame), sym.mtype
            else: return e.emitWRITEVAR(sym.name, sym.mtype, sym.value.value, o.frame), sym.mtype
        else:
            if type(sym.value) is CName: return e.emitGETSTATIC(sym.value.value + '/' + sym.name, sym.mtype, o.frame), sym.mtype
            else: return e.emitREADVAR(sym.name, sym.mtype, sym.value.value, o.frame), sym.mtype

    def visitArrayCell(self, ast, o):
        raise Exception("Arraycell found")

    def visitIntLiteral(self, ast, o):
        #ast: IntLiteral
        #o: Any
        ctxt = o
        frame = ctxt.frame
        return (e.emitPUSHICONST(ast.value, frame), IntType())

    def visitFloatLiteral(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        return e.emitPUSHFCONST(str(ast.value), frame), FloatType()

    def visitBooleanLiteral(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        return e.emitPUSHICONST(str(ast.value), frame), BoolType()

    def visitStringLiteral(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        a = e.emitPUSHCONST(str(ast.value), StringType(), frame), StringType()
        return e.emitPUSHCONST(str(ast.value), StringType(), frame), StringType()