import re
from ast import literal_eval
from typing import Tuple
from parsimonious import NodeVisitor, Grammar


class ValveVisitor(NodeVisitor):

    @staticmethod
    def visit_file(node, visited_children) -> dict:
        return dict(visited_children)

    @staticmethod
    def visit_dict(node, visited_children) -> dict:
        return dict(visited_children[1])

    @staticmethod
    def visit_pair(node, visited_children) -> Tuple:
        # Keys are case insensitive, so always make them lower case, otherwise we have a hard time using them in Python.
        key = visited_children[0][0].lower()
        value = visited_children[0][1]
        return key, value

    @staticmethod
    def visit_expr(node, visited_children):
        return visited_children[0][0]

    @staticmethod
    def visit_quoted(node, visited_children):
        result = literal_eval(node.match[0])
        return result

    def generic_visit(self, node, visited_children):
        return visited_children or node


grammar = Grammar(r"""
file        = pair+
dict        = dictOpen pair* dictClose
dictOpen    = "{" ws?
dictClose   = "}" ws?
pair        = (expr expr) / (expr dict)
expr        = (word / quoted) ws?
word        = ~r"[-\.\w]+"
quoted      = ~'"(?:[^"\\\\]|\\\\.)*"'
ws          = ~"\s*"
""")


visitor = ValveVisitor()

re_comments = re.compile(r'//.*')


def parse_valve_txt(source: str) -> dict:
    """
    Parse a Valve txt file (I don't know what this format is actually called).
    """
    # Remove comments before parsing.
    source = re_comments.sub('', source).strip()
    return visitor.visit(grammar.parse(source))


def load_valve_txt_file(file_name, encoding) -> dict:
    with open(file_name, 'r', encoding=encoding, errors="ignore") as f:
        return parse_valve_txt(f.read())
