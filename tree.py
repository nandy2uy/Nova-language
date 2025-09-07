class NumberNode:
    #Represents an integer number in the AST
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"NumberNode({self.value})"

class StringNode:
    #Represents a string literal in the AST
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f'StringNode("{self.value}")'
        
class BoolNode:
    """Represents a boolean literal i"""
    def __init__(self, token):
        self.token = token
        self.value = token.value == 'true'

    def __repr__(self):
        return f"BoolNode({self.value})"

class VarAccessNode:
    """Represents accessing the value of a variable."""
    def __init__(self, token):
        self.token = token
        self.name = token.value

    def __repr__(self):
        return f"VarAccessNode({self.name})"

class VarAssignNode:
    #variable declaraton
    def __init__(self, name_token, value_node):
        self.name_token = name_token
        self.value_node = value_node
        self.name = name_token.value

    def __repr__(self):
        return f"VarAssignNode({self.name}, {self.value_node})"

class BinOpNode:
    # a binary operation
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node
        self.op = op_token.value

    def __repr__(self):
        return f"({self.left_node} {self.op} {self.right_node})"

class PrintNode:
    # a print statement
    def __init__(self, value_node):
        self.value_node = value_node

    def __repr__(self):
        return f"PrintNode({self.value_node})"

class StatementsNode:
    #a block of statements, like in an if/else body."""
    def __init__(self):
        self.statements = []

    def __repr__(self):
        return f"StatementsNode([\n  " + ",\n  ".join(map(str, self.statements)) + "\n])"

class IfNode:
    # if-else 
    def __init__(self, condition_node, if_body_node, else_body_node=None):
        self.condition_node = condition_node
        self.if_body_node = if_body_node
        self.else_body_node = else_body_node

    def __repr__(self):
        else_str = f", else={self.else_body_node}" if self.else_body_node else ""
        return f"IfNode(if={self.condition_node}, then={self.if_body_node}{else_str})"

class WhileNode:
    #a while loop
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node

    def __repr__(self):
        return f"WhileNode(while={self.condition_node}, do={self.body_node})"

class FunctionDefNode:
    def __init__(self, name_token, arg_name_tokens, body_node): self.name_token, self.arg_name_tokens, self.body_node, self.name = name_token, arg_name_tokens, body_node, name_token.value
    def __repr__(self): return f"FunctionDefNode(name={self.name}, args={[t.value for t in self.arg_name_tokens]}, body={self.body_node})"

class FunctionCallNode:
    def __init__(self, name_token, arg_nodes): self.name_token, self.arg_nodes, self.name = name_token, arg_nodes, name_token.value
    def __repr__(self): return f"FunctionCallNode(name={self.name}, args={self.arg_nodes})"

class ReturnNode:
    def __init__(self, value_node): self.value_node = value_node
    def __repr__(self): return f"ReturnNode({self.value_node})"