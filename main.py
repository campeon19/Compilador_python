from antlr4 import *
from YAPLGrammarLexer import YAPLGrammarLexer
from YAPLGrammarParser import YAPLGrammarParser
from YAPLGrammarListener import YAPLGrammarListener
from antlr4.tree.Trees import Trees
import graphviz as gv

# correr lo siguiente en la terminal para crear el lexer y parser a partir de la gramatica YAPLGrammar.g4
# antlr4 YAPLGrammar.g4 -Dlanguage=Python3

# class SymbolTable:
#     def __init__(self):
#         self.symbols = {}

#     def add(self, name, type):
#         self.symbols[name] = type

#     def get_symbol_type(self, name):
#         return self.symbols[name]


class SymbolTableListener(YAPLGrammarListener):
    def __init__(self):
        self.symbol_table = {}

    def enterFeature(self, ctx: YAPLGrammarParser.FeatureContext):
        # if feature equal 3 children, it is a declaration
        # print(ctx.children)
        # print('si entra')
        if len(ctx.children) == 3:
            print('declaration')
            print(ctx.ID().getText())
            print(ctx.TYPE().getText())
            name = ctx.ID().getText()
            type = ctx.TYPE().getText()
            self.symbol_table[name] = type
        # if ctx.formal():
        #     print('formal')
        #     print(ctx.formal().getText())
        #     name = ctx.formal().getText()
        #     type = ctx.type().getText()
        #     self.symbol_table[name] = type


class TypeCheckerListener(YAPLGrammarListener):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table

    def get_expr_type(self, expr_ctx):
        if expr_ctx.TYPE() == 'INT':
            return 'INT'
        elif expr_ctx.ID():
            id = expr_ctx.ID()[0].getText()
            return self.symbol_table[id]
        else:
            left_type = self.get_expr_type(expr_ctx.expr(0))
            right_type = self.get_expr_type(expr_ctx.expr(1))
            if left_type == right_type:
                return left_type
            else:
                return 'error'

    def exitExpr(self, ctx: YAPLGrammarParser.ExprContext):
        if ctx.ADD() or ctx.MINUS() or ctx.MULTIPLY() or ctx.DIVISION():

            left_expr = ctx.expr(0)
            right_expr = ctx.expr(1)

            left_type = self.get_expr_type(left_expr)
            right_type = self.get_expr_type(right_expr)

            if left_type != 'INT' or right_type != 'INT':
                # print error message and shoe line number
                print('Error: Operands must be integers at line: ' +
                      str(ctx.start.line))
                # print('Error: Operands must be integers')
            elif left_type == 'error' or right_type == 'error':
                print('Error: Type mismatch')
        elif ctx.INTEGER_NEGATIVE():
            operand = ctx.expr(0)
            operand_type = self.get_expr_type(operand)
            if operand_type != 'INT':
                print('Error: Operand must be integer')
        elif ctx.ASSIGNMENT():
            left_expr = ctx.expr(0)
            right_expr = ctx.expr(1)

            left_type = self.get_expr_type(left_expr)
            right_type = right_expr[0].getText()

            if left_type != right_type:
                print('Error: Type mismatch')


def visualize_tree(tree):
    graph = gv.Digraph(format='png')
    add_nodes(graph, tree)
    add_edges(graph, tree)
    graph.render("tree")  # Guardar el árbol como imagen


def add_nodes(graph, tree):
    if tree is None:
        return
    node_id = str(hash(tree))
    if isinstance(tree, TerminalNode):
        node_label = tree.symbol.text
    else:
        node_label = tree.parser.ruleNames[tree.getRuleContext(
        ).getRuleIndex()]
    graph.node(node_id, label=node_label)
    for child in Trees.getChildren(tree):
        child_id = str(hash(child))
        add_nodes(graph, child)


def add_edges(graph, tree):
    if tree is None:
        return
    node_id = str(hash(tree))
    for child in Trees.getChildren(tree):
        child_id = str(hash(child))
        add_edges(graph, child)
        graph.edge(node_id, child_id)


def main():
    # read txt file
    with open('programa3.txt', 'r') as file:
        programa = file.read()

    lexer = YAPLGrammarLexer(InputStream(programa))
    parser = YAPLGrammarParser(CommonTokenStream(lexer))
    tree = parser.program()
    print(tree.toStringTree(recog=parser))
    visualize_tree(tree)

    # symbol table
    symbol_table_listener = SymbolTableListener()
    walker = ParseTreeWalker()
    walker.walk(symbol_table_listener, tree)

    print(symbol_table_listener.symbol_table)

    # type checker
    type_checker_listener = TypeCheckerListener(
        symbol_table_listener.symbol_table)
    walker.walk(type_checker_listener, tree)


if __name__ == '__main__':
    main()
