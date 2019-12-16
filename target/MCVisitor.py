# Generated from main/mc/parser/MC.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MCParser import MCParser
else:
    from MCParser import MCParser

# This class defines a complete generic visitor for a parse tree produced by MCParser.

class MCVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MCParser#program.
    def visitProgram(self, ctx:MCParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#decl.
    def visitDecl(self, ctx:MCParser.DeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#var_decl.
    def visitVar_decl(self, ctx:MCParser.Var_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#primi_type.
    def visitPrimi_type(self, ctx:MCParser.Primi_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#id_list.
    def visitId_list(self, ctx:MCParser.Id_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#identifier.
    def visitIdentifier(self, ctx:MCParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#id_array.
    def visitId_array(self, ctx:MCParser.Id_arrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#id_single.
    def visitId_single(self, ctx:MCParser.Id_singleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#func_decl.
    def visitFunc_decl(self, ctx:MCParser.Func_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#array_pointer_type.
    def visitArray_pointer_type(self, ctx:MCParser.Array_pointer_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#param_list.
    def visitParam_list(self, ctx:MCParser.Param_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#param_decl.
    def visitParam_decl(self, ctx:MCParser.Param_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#statement.
    def visitStatement(self, ctx:MCParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#if_stmt.
    def visitIf_stmt(self, ctx:MCParser.If_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#dowhile_stmt.
    def visitDowhile_stmt(self, ctx:MCParser.Dowhile_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#for_stmt.
    def visitFor_stmt(self, ctx:MCParser.For_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#break_stmt.
    def visitBreak_stmt(self, ctx:MCParser.Break_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#continue_stmt.
    def visitContinue_stmt(self, ctx:MCParser.Continue_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#return_stmt.
    def visitReturn_stmt(self, ctx:MCParser.Return_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#expression_stmt.
    def visitExpression_stmt(self, ctx:MCParser.Expression_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#block_stmt.
    def visitBlock_stmt(self, ctx:MCParser.Block_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#blockmem.
    def visitBlockmem(self, ctx:MCParser.BlockmemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#expression.
    def visitExpression(self, ctx:MCParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#expression1.
    def visitExpression1(self, ctx:MCParser.Expression1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#expression2.
    def visitExpression2(self, ctx:MCParser.Expression2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#expression3.
    def visitExpression3(self, ctx:MCParser.Expression3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#expression4.
    def visitExpression4(self, ctx:MCParser.Expression4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#expression5.
    def visitExpression5(self, ctx:MCParser.Expression5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#expression6.
    def visitExpression6(self, ctx:MCParser.Expression6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#expression7.
    def visitExpression7(self, ctx:MCParser.Expression7Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#expression8.
    def visitExpression8(self, ctx:MCParser.Expression8Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#expression9.
    def visitExpression9(self, ctx:MCParser.Expression9Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#operand.
    def visitOperand(self, ctx:MCParser.OperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#literal.
    def visitLiteral(self, ctx:MCParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#func_call.
    def visitFunc_call(self, ctx:MCParser.Func_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#param_list_call.
    def visitParam_list_call(self, ctx:MCParser.Param_list_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MCParser#param_call.
    def visitParam_call(self, ctx:MCParser.Param_callContext):
        return self.visitChildren(ctx)



del MCParser