from antlr4 import *
from YAPLGrammarLexer import YAPLGrammarLexer
from YAPLGrammarParser import YAPLGrammarParser
from antlr4.tree.Trees import Trees
import graphviz as gv

# correr lo siguiente en la terminal para crear el lexer y parser a partir de la gramatica YAPLGrammar.g4
# antlr4 YAPLGrammar.g4 -Dlanguage=Python3


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


if __name__ == '__main__':
    main()
