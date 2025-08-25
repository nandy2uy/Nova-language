# interpreter.py
from tree import NumberNode, StringNode, BoolNode, VarAccessNode, VarAssignNode, BinOpNode, PrintNode, StatementsNode, IfNode

class SymbolTable:
    """A symbol table to store variable values."""
    def __init__(self):
        self.symbols = {}

    def get(self, name):
        """Get a value from the symbol table."""
        value = self.symbols.get(name, None)
        if value is None:
            raise NameError(f"Variable '{name}' is not defined.")
        return value

    def set(self, name, value):
        """Set a value in the symbol table."""
        self.symbols[name] = value

class Interpreter:
    """
    The interpreter, responsible for executing the code from the AST.
    """
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit(self, node):
        """The main visit method, which dispatches to other visit methods."""
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        """Called if no specific visit method is found for a node type."""
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node):
        return node.value

    def visit_StringNode(self, node):
        return node.value
        
    def visit_BoolNode(self, node):
        return node.value

    def visit_VarAccessNode(self, node):
        return self.symbol_table.get(node.name)

    def visit_VarAssignNode(self, node):
        value = self.visit(node.value_node)
        self.symbol_table.set(node.name, value)
        return value

    def visit_BinOpNode(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)

        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            # Basic division, add check for division by zero
            if right == 0:
                raise Exception("Runtime error: Division by zero.")
            return left / right
        elif node.op == '==':
            return left == right
        elif node.op == '!=':
            return left != right
        elif node.op == '<':
            return left < right
        elif node.op == '>':
            return left > right
            
        raise Exception(f"Unknown operator: {node.op}")

    def visit_PrintNode(self, node):
        value = self.visit(node.value_node)
        print(value) # This is where the actual output happens
        return value

    def visit_StatementsNode(self, node):
        result = None
        for statement in node.statements:
            result = self.visit(statement)
        return result

    def visit_IfNode(self, node):
        condition = self.visit(node.condition_node)
        if condition:
            return self.visit(node.if_body_node)
        elif node.else_body_node:
            return self.visit(node.else_body_node)
