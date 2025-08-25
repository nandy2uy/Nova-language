# parser.py
from lexer import TT_INT, TT_KEYWORD, TT_IDENTIFIER, TT_OPERATOR, TT_STRING, TT_LBRACE, TT_RBRACE, TT_LPAREN, TT_RPAREN, TT_COMMA, TT_EOF
from tree import NumberNode, StringNode, BoolNode, VarAccessNode, VarAssignNode, BinOpNode, PrintNode, StatementsNode, IfNode, WhileNode, FunctionDefNode, FunctionCallNode, ReturnNode

class Parser:
    def __init__(self, tokens):
        self.tokens, self.pos, self.current_token = tokens, 0, tokens[0]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens): self.current_token = self.tokens[self.pos]
        return self.current_token

    def parse(self): return self.statements()

    def statements(self):
        stmts = StatementsNode()
        while self.current_token.type not in (TT_EOF, TT_RBRACE):
            stmts.statements.append(self.statement())
        return stmts

    def statement(self):
        if self.current_token.type == TT_KEYWORD:
            if self.current_token.value == 'let': return self.parse_let_statement()
            if self.current_token.value == 'print': return self.parse_print_statement()
            if self.current_token.value == 'if': return self.parse_if_statement()
            if self.current_token.value == 'while': return self.parse_while_statement()
            if self.current_token.value == 'fun': return self.parse_function_definition()
            if self.current_token.value == 'return': return self.parse_return_statement()
        return self.expression()

    def parse_let_statement(self):
        self.advance()
        if self.current_token.type != TT_IDENTIFIER: raise Exception("Expected identifier")
        name = self.current_token
        self.advance()
        if self.current_token.value != '=': raise Exception("Expected '='")
        self.advance()
        value = self.expression()
        return VarAssignNode(name, value)
    
    def parse_print_statement(self):
        self.advance()
        return PrintNode(self.expression())

    def parse_if_statement(self):
        self.advance()
        cond = self.expression()
        if self.current_token.type != TT_LBRACE: raise Exception("Expected '{'")
        self.advance()
        if_body = self.statements()
        if self.current_token.type != TT_RBRACE: raise Exception("Expected '}'")
        self.advance()
        else_body = None
        if self.current_token.value == 'else':
            self.advance()
            if self.current_token.type != TT_LBRACE: raise Exception("Expected '{'")
            self.advance()
            else_body = self.statements()
            if self.current_token.type != TT_RBRACE: raise Exception("Expected '}'")
            self.advance()
        return IfNode(cond, if_body, else_body)

    def parse_while_statement(self):
        self.advance()
        cond = self.expression()
        if self.current_token.type != TT_LBRACE: raise Exception("Expected '{'")
        self.advance()
        body = self.statements()
        if self.current_token.type != TT_RBRACE: raise Exception("Expected '}'")
        self.advance()
        return WhileNode(cond, body)

    def parse_function_definition(self):
        self.advance() # 'fun'
        if self.current_token.type != TT_IDENTIFIER: raise Exception("Expected function name")
        name = self.current_token
        self.advance()
        if self.current_token.type != TT_LPAREN: raise Exception("Expected '('")
        self.advance()
        args = []
        if self.current_token.type != TT_RPAREN:
            args.append(self.current_token)
            self.advance()
            while self.current_token.type == TT_COMMA:
                self.advance()
                if self.current_token.type != TT_IDENTIFIER: raise Exception("Expected argument name")
                args.append(self.current_token)
                self.advance()
        if self.current_token.type != TT_RPAREN: raise Exception("Expected ')' or ','")
        self.advance()
        if self.current_token.type != TT_LBRACE: raise Exception("Expected '{'")
        self.advance()
        body = self.statements()
        if self.current_token.type != TT_RBRACE: raise Exception("Expected '}'")
        self.advance()
        return FunctionDefNode(name, args, body)

    def parse_return_statement(self):
        self.advance()
        return ReturnNode(self.expression())

    def expression(self):
        node = self.term()
        while self.current_token.value in ('+', '-', '==', '!=', '<', '>'):
            op = self.current_token; self.advance(); node = BinOpNode(node, op, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.value in ('*', '/'):
            op = self.current_token; self.advance(); node = BinOpNode(node, op, self.factor())
        return node

    def factor(self):
        token = self.current_token
        if token.type == TT_INT: self.advance(); return NumberNode(token)
        if token.type == TT_STRING: self.advance(); return StringNode(token)
        if token.value in ('true', 'false'): self.advance(); return BoolNode(token)
        if token.type == TT_IDENTIFIER:
            self.advance()
            if self.current_token.type == TT_LPAREN: # Function call
                self.advance()
                arg_nodes = []
                if self.current_token.type != TT_RPAREN:
                    arg_nodes.append(self.expression())
                    while self.current_token.type == TT_COMMA:
                        self.advance()
                        arg_nodes.append(self.expression())
                if self.current_token.type != TT_RPAREN: raise Exception("Expected ')' or ','")
                self.advance()
                return FunctionCallNode(token, arg_nodes)
            return VarAccessNode(token) # Variable access
        raise Exception(f"Invalid syntax: {token}")