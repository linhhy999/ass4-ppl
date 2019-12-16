# 1711947 - Hy Phạm Ngọc Linh

from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *

class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

def flatten(lst):
        if lst==[]:
            return lst
        return lst[0]+flatten(lst[1:])

def isAssigned(ast,funcParam,funcCallParam):
    if type(funcParam) is ArrayPointerType:
        if ((not (type(funcCallParam) is ArrayPointerType)) \
            and (not (type(funcCallParam) is ArrayType))) \
            or (type(funcParam.eleType) != type(funcCallParam.eleType)):
            raise TypeMismatchInExpression(ast)
    elif type(funcParam) is FloatType:
        if (not (type(funcCallParam) is FloatType)) and (not (type(funcCallParam) is IntType)):
            raise TypeMismatchInExpression(ast)
    elif type(funcParam) != type(funcCallParam):
        raise TypeMismatchInExpression(ast)

class Symbol:
    def __init__(self,name,mtype,isCalled=False):
        self.name = name
        self.mtype = mtype
        self.isCalled = isCalled

class StaticChecker(BaseVisitor,Utils):

    global_envi = [
        Symbol("getInt",     MType([],IntType()),True),
        Symbol("putInt",     MType([IntType()],VoidType()),True),
        Symbol("putIntLn",   MType([IntType()],VoidType()),True),
        Symbol("getFloat",   MType([],FloatType()),True),
        Symbol("putFloat",   MType([FloatType()],VoidType()),True),
        Symbol("putFloatLn", MType([FloatType()],VoidType()),True),
        Symbol("putBool",    MType([BoolType()],VoidType()),True),
        Symbol("putBoolLn",  MType([BoolType()],VoidType()),True),
        Symbol("putString",  MType([StringType()],VoidType()),True),
        Symbol("putStringLn",MType([StringType()],VoidType()),True),
        Symbol("putLn",      MType([],VoidType()),True)
    ]
    __currentFuncType = VoidType()
    __isInLoop = False
    __currentFuncName = ''

    def __init__(self,ast):
        #print(ast)
        #print(ast)
        #print()
        self.ast = ast

    def check(self):
        self.visit(self.ast,[StaticChecker.global_envi[:]])
        return []

    def visitProgram(self,ast, c):
        for x in ast.decl:
            if type(x) is VarDecl:
                c[0]+=[self.visit(x,c[:])]
            else:
                if self.lookup(x.name.name,c[0],lambda q: q.name):
                    raise Redeclared(Function(),x.name.name)
                c[0]+=[Symbol(x.name.name,MType([i.varType for i in x.param],x.returnType))]
        mainFunc = self.lookup('main',c[0],lambda q: q.name)
        if mainFunc:
            if type(mainFunc.mtype) is MType:
                pass
            else:
                raise NoEntryPoint()
        else:
            raise NoEntryPoint()
        for x in ast.decl:
            if not (type(x) is VarDecl):
                self.visit(x,c[:])
        for x in c[-1]:
            if type(x.mtype) is MType:
                if (not x.isCalled) and (x.name != 'main'):
                    raise UnreachableFunction(x.name)

    def visitVarDecl(self,ast, c):
        if self.lookup(ast.variable,c[0],lambda q: q.name):
            raise Redeclared(Variable(),ast.variable)
        return Symbol(ast.variable,ast.varType)

    def visitFuncDecl(self,ast, c):
        temp = Symbol(ast.name.name,MType([x.varType for x in ast.param],ast.returnType))
        self.__currentFuncType = ast.returnType
        self.__currentFuncName = ast.name.name
        c=[[]]+c
        isReturn = True
        for x in ast.param:
            if self.lookup(x.variable,c[0],lambda q: q.name) == None:
                c[0]+=[self.visit(x,c[:])]
            else:
                raise Redeclared(Parameter(),x.variable)
        for x in ast.body.member:
            if type(x) is VarDecl:
                c[0]+=[self.visit(x,c[:])]
            else:
                self.visit(x,c[:])
        if not (type(ast.returnType) is VoidType):
            isReturn = False or self.visit(ast.body,c[:])
        if not isReturn:
            raise FunctionNotReturn(ast.name.name)
        self.__currentFuncName = ''
        self.__currentFuncType = None

    def visitBlock(self, ast, c):
        c=[[]]+c
        isReturn = False
        for x in ast.member:
            if type(x) is VarDecl:
                c[0]+=[self.visit(x,c[:])]
            else:
                if type(self.visit(x,c[:])) is bool:
                    isReturn = isReturn or self.visit(x,c[:])
        return isReturn

    def visitIf(self, ast, c):
        checkThen = False
        checkElse = False
        if not (type(self.visit(ast.expr,c[:])) is BoolType):
            raise TypeMismatchInStatement(ast)
        if type(self.visit(ast.thenStmt,c[:])) is bool:
            checkThen = checkThen or self.visit(ast.thenStmt,c[:])
        if ast.elseStmt:
            if type(self.visit(ast.elseStmt,c[:])) is bool:
                checkElse = checkElse or self.visit(ast.elseStmt,c[:])
        return checkThen and checkElse

    def visitReturn(self, ast, c):
        if ast.expr == None:
            if not (type(self.__currentFuncType) is VoidType):
                raise TypeMismatchInStatement(ast)
        else:
            retStmtType = self.visit(ast.expr,c[:])
            if (type(self.__currentFuncType) is FloatType) and (type(retStmtType) is IntType):
                pass
            elif type(self.__currentFuncType) is ArrayPointerType: 
                if ((not (type(retStmtType) is ArrayType)) \
                    and (not (type(retStmtType) is ArrayPointerType))) \
                    or (type(self.__currentFuncType.eleType) != type(retStmtType.eleType)):
                    raise TypeMismatchInStatement(ast)
            else:
                if type(self.__currentFuncType) != type(retStmtType):
                    raise TypeMismatchInStatement(ast)
        return True

    def visitFor(self, ast, c):
        e1 = self.visit(ast.expr1,c[:])
        e2 = self.visit(ast.expr2,c[:])
        e3 = self.visit(ast.expr3,c[:])
        if (not (type(e1) is IntType)) or (not (type(e2) is BoolType)) \
            or (not (type(e3) is IntType)):
            raise TypeMismatchInStatement(ast)
        preThis = self.__isInLoop
        self.__isInLoop = True
        self.visit(ast.loop,c[:])
        self.__isInLoop = preThis

    def visitDowhile(self, ast, c):
        if not (type(self.visit(ast.exp,c[:])) is BoolType):
            raise TypeMismatchInStatement(ast)
        preThis = self.__isInLoop
        self.__isInLoop = True
        isReturn = False
        for x in ast.sl:
            temp = self.visit(x,c[:])
            if type(temp) is bool:
                isReturn = isReturn or self.visit(x,c[:])
        self.__isInLoop = preThis
        return isReturn

    def visitBreak(self, ast, c):
        if not self.__isInLoop:
            raise BreakNotInLoop()

    def visitContinue(self, ast, c):
        if not self.__isInLoop:
            raise ContinueNotInLoop()

    def visitArrayCell(self, ast, c):
        idType = self.visit(ast.arr,c[:])
        if type(self.visit(ast.idx,c[:])) is IntType \
           and (type(idType) is ArrayType or type(idType) is ArrayPointerType) :
            return idType.eleType
        raise TypeMismatchInExpression(ast)

    def visitBinaryOp(self, ast, c):
        left = self.visit(ast.left,c)
        right = self.visit(ast.right,c)
        if ast.op == '=':
            if (not (type(ast.left) is Id)) and (not (type(ast.left) is ArrayCell)):
                raise NotLeftValue(ast.left)
        if type(left) != type(right):
            if type(left) is IntType and type(right) is FloatType:
                if ast.op == '=':
                    raise TypeMismatchInExpression(ast)
                left, right = right, left
            elif type(left) is FloatType and type(right) is IntType: 
                pass
            else: raise TypeMismatchInExpression(ast)
        if type(left) is BoolType:
            if ast.op in ['||','&&','==','!=','=']:
                return BoolType()
        elif type(left) is IntType:
            if ast.op in ['<','<=','>','>=','==','!=']:
                return BoolType()
            elif ast.op in ['+','-','*','/','%','=']:
                return IntType()
        elif type(left) is FloatType:
            if ast.op in ['+','-','*','/']:
                return FloatType()
            elif ast.op in ['<','<=','>','>=']:
                return BoolType()
            elif ast.op == '=':
                return FloatType()
        elif type(left) is StringType:
            if ast.op == '=':
                return StringType()
        raise TypeMismatchInExpression(ast)

    def visitUnaryOp(self, ast, c):
        operand = self.visit(ast.body,c[:])
        if ast.op == '!' and type(operand) is BoolType:
            return BoolType()
        if ast.op == '-' :
            if type(operand) is IntType:
                return IntType()
            if type(operand) is FloatType:
                return FloatType()
        raise TypeMismatchInExpression(ast)

    def visitCallExpr(self, ast, c):
        temp = self.lookup(ast.method.name,flatten(c),lambda q: q.name)
        if temp == None:
            raise Undeclared(Function(),ast.method.name)
        elif not (type(temp.mtype) is MType):
            raise TypeMismatchInExpression(ast)
        funcCallParam = []
        funcParam = temp.mtype.partype
        for x in ast.param:
            funcCallParam += [self.visit(x,c[:])]
        if len(funcCallParam) != len(funcParam):
            raise TypeMismatchInExpression(ast)
        else:
            for i in range(len(funcCallParam)):
                isAssigned(ast,funcParam[i],funcCallParam[i])
        if temp.name != self.__currentFuncName:
            temp.isCalled = True
        return temp.mtype.rettype

    def visitId(self, ast, c):
        temp = self.lookup(ast.name,flatten(c),lambda q: q.name)
        if temp == None:
            raise Undeclared(Identifier(),ast.name)
        elif type(temp.mtype) is MType:
            raise TypeMismatchInExpression(ast)
        return temp.mtype

    def visitIntLiteral(self,ast, c): 
        return IntType()

    def visitFloatLiteral(self,ast, c): 
        return FloatType()

    def visitBooleanLiteral(self,ast, c): 
        return BoolType()

    def visitStringLiteral(self,ast, c): 
        return StringType()
