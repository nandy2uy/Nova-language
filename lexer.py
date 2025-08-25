# lexer.py

class Token:
    """A simple class to represent a token."""
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        """String representation of the class instance."""
        return f"Token({self.type}, {repr(self.value)})"

# Define token types as constants
TT_INT        = 'INT'
TT_KEYWORD    = 'KEYWORD'
TT_IDENTIFIER = 'IDENTIFIER'
TT_OPERATOR   = 'OPERATOR'
TT_STRING     = 'STRING'
TT_LBRACE     = 'LBRACE'    # {
TT_RBRACE     = 'RBRACE'    # }
TT_LPAREN     = 'LPAREN'    # (
TT_RPAREN     = 'RPAREN'    # )
TT_COMMA      = 'COMMA'     # ,
TT_EOF        = 'EOF'       # End of File

# Keywords in the Nova language
KEYWORDS = [
    'let', 'if', 'else', 'print', 'true', 'false', 'while',
    'fun', 'return'
]

class Lexer:
    """The lexer, responsible for breaking code into tokens."""
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(TT_INT, int(result))

    def string(self):
        result = ''
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()
        return Token(TT_STRING, result)

    def identifier(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        
        return Token(TT_KEYWORD, result) if result in KEYWORDS else Token(TT_IDENTIFIER, result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace(): self.skip_whitespace(); continue
            if self.current_char == '/' and self.peek() == '/': self.skip_comment(); continue
            if self.current_char.isdigit(): return self.number()
            if self.current_char.isalpha(): return self.identifier()
            if self.current_char == '"': return self.string()

            if self.current_char == '=' and self.peek() == '=': self.advance(); self.advance(); return Token(TT_OPERATOR, '==')
            if self.current_char == '!' and self.peek() == '=': self.advance(); self.advance(); return Token(TT_OPERATOR, '!=')

            if self.current_char in ['=', '+', '-', '*', '/', '<', '>']:
                op = self.current_char; self.advance(); return Token(TT_OPERATOR, op)
            
            # --- THIS IS THE CORRECTED PART ---
            if self.current_char == '{': self.advance(); return Token(TT_LBRACE, '{')
            if self.current_char == '}': self.advance(); return Token(TT_RBRACE, '}')
            if self.current_char == '(': self.advance(); return Token(TT_LPAREN, '(')
            if self.current_char == ')': self.advance(); return Token(TT_RPAREN, ')')
            if self.current_char == ',': self.advance(); return Token(TT_COMMA, ',')
            # ------------------------------------

            raise Exception(f"Invalid character: '{self.current_char}'")

        return Token(TT_EOF, None)

    def peek(self):
        peek_pos = self.pos + 1
        return self.text[peek_pos] if peek_pos < len(self.text) else None

    def tokenize(self):
        tokens = []
        token = self.get_next_token()
        while token.type != TT_EOF:
            tokens.append(token)
            token = self.get_next_token()
        tokens.append(token)
        return tokens
