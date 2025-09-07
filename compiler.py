#from tree import NumberNode, StringNode, BoolNode, VarAccessNode, VarAssignNode, BinOpNode, PrintNode, StatementsNode, IfNode
from tree import NumberNode, StringNode, BoolNode, VarAccessNode, VarAssignNode, BinOpNode, PrintNode, StatementsNode, IfNode, WhileNode


#    The compiler, responsible for translating the AST into bytecode.

class Compiler:
    def __init__(self):
        self.bytecode = []
        self.functions = {}

    def compile(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit method for {type(node).__name__}')

    def visit_NumberNode(self, node): self.bytecode.append(('PUSH', node.value))
    def visit_StringNode(self, node): self.bytecode.append(('PUSH', node.value))
    def visit_BoolNode(self, node): self.bytecode.append(('PUSH', node.value))
    def visit_VarAccessNode(self, node): self.bytecode.append(('LOAD', node.name))
    
    def visit_VarAssignNode(self, node):
        self.compile(node.value_node)
        self.bytecode.append(('STORE', node.name))

    def visit_BinOpNode(self, node):
        self.compile(node.left_node)
        self.compile(node.right_node)
        # FIX: Use word-based opcodes
        if node.op == '+': self.bytecode.append(('ADD', None))
        elif node.op == '-': self.bytecode.append(('SUB', None))
        elif node.op == '*': self.bytecode.append(('MUL', None))
        elif node.op == '/': self.bytecode.append(('DIV', None))
        elif node.op in ('==', '!=', '<', '>'):
            self.bytecode.append(('COMPARE', node.op))
        else: raise Exception(f"Unknown operator {node.op}")

    def visit_PrintNode(self, node):
        self.compile(node.value_node)
        self.bytecode.append(('PRINT', None))

    def visit_StatementsNode(self, node):
        for stmt in node.statements: self.compile(stmt)

    def visit_IfNode(self, node):
        self.compile(node.condition_node)
        self.bytecode.append(('JUMP_IF_FALSE', 'placeholder'))
        false_idx = len(self.bytecode) - 1
        self.compile(node.if_body_node)
        jump_idx = -1
        if node.else_body_node:
            self.bytecode.append(('JUMP', 'placeholder'))
            jump_idx = len(self.bytecode) - 1
        self.bytecode[false_idx] = ('JUMP_IF_FALSE', len(self.bytecode))
        if node.else_body_node:
            self.compile(node.else_body_node)
            self.bytecode[jump_idx] = ('JUMP', len(self.bytecode))

    def visit_WhileNode(self, node):
        start_pos = len(self.bytecode)
        self.compile(node.condition_node)
        self.bytecode.append(('JUMP_IF_FALSE', 'placeholder'))
        false_idx = len(self.bytecode) - 1
        self.compile(node.body_node)
        self.bytecode.append(('JUMP', start_pos))
        self.bytecode[false_idx] = ('JUMP_IF_FALSE', len(self.bytecode))

    def visit_FunctionDefNode(self, node):
        self.bytecode.append(('JUMP', 'placeholder'))
        jump_idx = len(self.bytecode) - 1
        start_pos = len(self.bytecode)
        self.functions[node.name] = {'start_pos': start_pos, 'args': [t.value for t in node.arg_name_tokens]}
        self.compile(node.body_node)
        self.bytecode.append(('PUSH', None)) 
        self.bytecode.append(('RETURN', None))
        self.bytecode[jump_idx] = ('JUMP', len(self.bytecode))

    def visit_FunctionCallNode(self, node):
        for arg in node.arg_nodes: self.compile(arg)
        self.bytecode.append(('CALL', node.name))

    def visit_ReturnNode(self, node):
        self.compile(node.value_node)
        self.bytecode.append(('RETURN', None))

