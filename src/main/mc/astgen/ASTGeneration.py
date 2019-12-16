#1711947 - Hy Pham Ngoc Linh

from MCVisitor import MCVisitor
from MCParser import MCParser
from AST import *

class ASTGeneration(MCVisitor):
    def visitProgram(self,ctx:MCParser.ProgramContext):
        return Program([j for i in ctx.decl() for j in self.visit(i)])

    def visitDecl(self,ctx:MCParser.DeclContext):
        return self.visit(ctx.var_decl()) if ctx.var_decl()\
                else [self.visit(ctx.func_decl())]

    def visitVar_decl(self,ctx:MCParser.Var_declContext):
        type = self.visit(ctx.primi_type())
        vardecls = []
        for i in ctx.id_list().identifier():
            if i.id_single(): 
                vardecls += [VarDecl(i.id_single().ID().getText(), type)]
            else: 
                vardecls += [VarDecl(i.id_array().ID().getText(), ArrayType(int(i.id_array().INTLIT().getText()), type))]
        return vardecls
    
    def visitPrimi_type(self,ctx:MCParser.Primi_typeContext):
        if ctx.INTTYPE():
            return IntType()
        if ctx.BOOLTYPE():
            return BoolType()
        if ctx.FLOATTYPE():
            return FloatType()
        if ctx.STRINGTYPE():
            return StringType()
    
    def visitFunc_decl(self, ctx:MCParser.Func_declContext):
        name = Id(ctx.ID().getText())
        if ctx.primi_type():
            returnType = self.visit(ctx.primi_type())
        else:
            if ctx.VOIDTYPE():
                returnType = VoidType()
            else:
                returnType = self.visit(ctx.array_pointer_type())
        param = [] if ctx.param_list()==None else self.visit(ctx.param_list())
        body = self.visit(ctx.block_stmt())
        return FuncDecl(name,param,returnType,body)
    
    def visitArray_pointer_type(self, ctx:MCParser.Array_pointer_typeContext):
        return ArrayPointerType(self.visit(ctx.primi_type()))

    def visitParam_list(self, ctx:MCParser.Param_listContext):
        return [self.visit(i) for i in ctx.param_decl()]

    def visitParam_decl(self, ctx:MCParser.Param_declContext):
        type = ArrayPointerType(self.visit(ctx.primi_type())) if ctx.LSB() else self.visit(ctx.primi_type())
        return VarDecl(ctx.ID().getText(),type)

    def visitStatement(self, ctx:MCParser.StatementContext):
        return self.visit(ctx.getChild(0))

    def visitIf_stmt(self, ctx:MCParser.If_stmtContext):
        expr = self.visit(ctx.expression())
        thenStmt = self.visit(ctx.getChild(4))
        elseStmt = self.visit(ctx.getChild(6)) if ctx.ELSE() else None
        return If(expr,thenStmt,elseStmt)

    def visitDowhile_stmt(self, ctx:MCParser.Dowhile_stmtContext):
        sl = [self.visit(i) for i in ctx.statement()]
        exp = self.visit(ctx.expression())
        return Dowhile(sl,exp)

    def visitFor_stmt(self, ctx:MCParser.For_stmtContext):
        expr1 = self.visit(ctx.getChild(2))
        expr2 = self.visit(ctx.getChild(4))
        expr3 = self.visit(ctx.getChild(6))
        loop = self.visit(ctx.statement())
        return For(expr1, expr2, expr3, loop)

    def visitBreak_stmt(self, ctx:MCParser.Break_stmtContext):
        return Break()

    def visitContinue_stmt(self, ctx:MCParser.Continue_stmtContext):
        return Continue()

    def visitReturn_stmt(self, ctx:MCParser.Return_stmtContext):
        expr = self.visit(ctx.expression()) if ctx.expression() else None
        return Return(expr)

    def visitExpression_stmt(self, ctx:MCParser.Expression_stmtContext):
        return self.visit(ctx.expression())

    def visitBlock_stmt(self, ctx:MCParser.Block_stmtContext):
        return Block([j for i in ctx.blockmem() for j in self.visit(i)])
    
    def visitBlockmem(self, ctx:MCParser.BlockmemContext):
        return self.visit(ctx.var_decl()) if ctx.var_decl() else [self.visit(ctx.statement())]
    
    def visitExpression(self, ctx:MCParser.ExpressionContext):
        if ctx.ASSIGNOP():
            op = ctx.ASSIGNOP().getText()
            left = self.visit(ctx.expression1())
            right = self.visit(ctx.expression())
            return BinaryOp(op, left, right) 
        else: return self.visit(ctx.expression1())

    def visitExpression1(self, ctx:MCParser.Expression1Context):
        if ctx.OROP():
            op = ctx.OROP().getText()
            left = self.visit(ctx.expression1())
            right = self.visit(ctx.expression2())
            return BinaryOp(op, left, right) 
        else: return self.visit(ctx.expression2())

    def visitExpression2(self, ctx:MCParser.Expression2Context):
        if ctx.ANDOP():
            op = ctx.ANDOP().getText()
            left = self.visit(ctx.expression2())
            right = self.visit(ctx.expression3())
            return BinaryOp(op, left, right) 
        else: return self.visit(ctx.expression3())

    def visitExpression3(self, ctx:MCParser.Expression3Context):
        if ctx.EQUALOP() or ctx.NOTEQUALOP():
            op = ctx.getChild(1).getText()
            left = self.visit(ctx.expression4()[0])
            right = self.visit(ctx.expression4()[1])
            return BinaryOp(op, left, right)
        else: return self.visit(ctx.expression4()[0])

    def visitExpression4(self, ctx:MCParser.Expression4Context):
        if ctx.LESSOP() or ctx.GREATEROP() or ctx.LEOP() or ctx.GEOP():
            op = ctx.getChild(1).getText()
            left = self.visit(ctx.expression5()[0])
            right = self.visit(ctx.expression5()[1])
            return BinaryOp(op, left, right) 
        else: return self.visit(ctx.expression5()[0])

    def visitExpression5(self, ctx:MCParser.Expression5Context):
        if ctx.ADDOP() or ctx.SUBOP():
            op = ctx.getChild(1).getText()
            left = self.visit(ctx.expression5())
            right = self.visit(ctx.expression6())
            return BinaryOp(op, left, right) 
        else: return self.visit(ctx.expression6())

    def visitExpression6(self, ctx:MCParser.Expression6Context):
        if ctx.DIVOP() or ctx.MULOP() or ctx.MODOP():
            op = ctx.getChild(1).getText()
            left = self.visit(ctx.expression6())
            right = self.visit(ctx.expression7())
            return BinaryOp(op, left, right) 
        else: return self.visit(ctx.expression7())

    def visitExpression7(self, ctx:MCParser.Expression7Context):
        if ctx.SUBOP() or ctx.NOTOP():
            op = ctx.getChild(0).getText()
            body = self.visit(ctx.expression7())
            return UnaryOp(op, body)
        else: return self.visit(ctx.expression8())

    def visitExpression8(self, ctx:MCParser.Expression8Context):
        if ctx.LSB():
            arr = self.visit(ctx.expression8())
            idx = self.visit(ctx.expression())
            return ArrayCell(arr, idx)
        else: return self.visit(ctx.expression9())

    def visitExpression9(self, ctx:MCParser.Expression9Context):
        if ctx.LB():
            return self.visit(ctx.expression())
        else: return self.visit(ctx.operand())

    def visitOperand(self, ctx:MCParser.OperandContext):
        return self.visit(ctx.getChild(0))

    def visitLiteral(self, ctx:MCParser.LiteralContext):
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        if ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        if ctx.STRINGLIT():
            return StringLiteral(ctx.STRINGLIT().getText())
        if ctx.BOOLLIT():
            if (ctx.BOOLLIT().getText()=='true'):
                boollit = True
            else: boollit = False
            return BooleanLiteral(boollit)
    
    def visitFunc_call(self, ctx:MCParser.Func_callContext):
        method = Id(ctx.ID().getText())
        param = self.visit(ctx.param_list_call()) if ctx.param_list_call() else []
        return CallExpr(method, param)

    def visitParam_list_call(self, ctx:MCParser.Param_list_callContext):
        return [self.visit(i) for i in ctx.param_call()]

    def visitParam_call(self, ctx:MCParser.Param_callContext):
        return self.visit(ctx.getChild(0))
        
    def visitIdentifier(self,ctx:MCParser.IdentifierContext):
        return self.visit(ctx.getChild(0))
    
    def visitId_array(self,ctx:MCParser.Id_arrayContext):
        return ArrayCell(Id(ctx.ID().getText()),IntLiteral(int(ctx.INTLIT().getText())))
    
    def visitId_single(self,ctx:MCParser.Id_singleContext):
        return Id(ctx.ID().getText())
