import re
from .tokens import tokens

class Token:
    def __init__(self, token_type, value, number_line):
        self.type = token_type  
        self.value = value      
        self.number_line = number_line        

    def __repr__(self):
        return f'Token({self.type}, {self.value}, Line: {self.line})'
    
    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "number_line": self.number_line
        }

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.position = 0
        self.number_line = 1  # Iniciar el contador de líneas

    def tokenize(self):
        while self.position < len(self.code):
            match = None
            for token_type, token_regex in tokens:
                regex = re.compile(token_regex)
                match = regex.match(self.code, self.position)
                if match:
                    text = match.group(0)
                    if token_type == 'WHITESPACE':
                        self.number_line += text.count('\n')  # Contar nuevas líneas
                    elif token_type != 'WHITESPACE':
                        # Crear un nuevo objeto Token y agregarlo a la lista de tokens
                        self.tokens.append(Token(token_type, text, self.number_line))
                    self.position = match.end(0)
                    break
            if not match:
                raise SyntaxError(f'Error de sintaxis en la línea {self.number_line}: token no reconocido en "{self.code[self.position:]}"')
        return self.tokens