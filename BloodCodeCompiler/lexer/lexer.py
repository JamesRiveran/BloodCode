import re
from BloodCodeCompiler.tokens import tokens

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.pos = 0

    def tokenize(self):
        while self.pos < len(self.code):
            match = None
            for token_type, token_regex in tokens:
                regex = re.compile(token_regex)
                match = regex.match(self.code, self.pos)
                if match:
                    text = match.group(0)
                    if token_type != 'WHITESPACE' and token_type != 'COMMENT':
                        self.tokens.append((token_type, text))
                    self.pos = match.end(0)
                    break
            if not match:
                raise SyntaxError(f'Error de sintaxis: token no reconocido en "{self.code[self.pos:]}"')
        return self.tokens
