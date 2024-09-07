from .ast import ASTNode, NumberNode, IdentifierNode, BinaryOpNode, StringNode, DeclarationNode, BlockNode, IfStatementNode, LoopNode, FunctionCallNode, RestNode

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

    def expect(self, token_type):
        if self.current_token[0] == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Se esperaba {token_type}, pero se encontró {self.current_token[0]}")

    def parse(self):
        return self.parse_block()

    def parse_block(self):
        statements = []
        self.expect('LBRACE')
        while self.current_token[0] != 'RBRACE':
            statements.append(self.parse_statement())
        self.expect('RBRACE')
        return BlockNode(statements)

    def parse_statement(self):
        if self.current_token[0] == 'HUNTER':
            return self.parse_declaration()
        elif self.current_token[0] == 'INSIGHT':
            return self.parse_if_statement()
        elif self.current_token[0] == 'NIGHTMARE':
            return self.parse_nightmare_loop()
        elif self.current_token[0] == 'DREAM':
            return self.parse_dream_loop()  
        elif self.current_token[0] == 'PRAY':
            return self.parse_pray()
        elif self.current_token[0] == 'REST':
            return self.parse_rest_statement()
        elif self.current_token[0] == 'IDENTIFIER': 
            return self.parse_assignment_or_expression()
        else:
            return self.parse_expression()

    def parse_dream_loop(self):
        self.expect('DREAM')
        self.expect('LPAREN')
        condition = self.parse_expression()
        self.expect('RPAREN')
        block = self.parse_block()  
        return LoopNode(None, condition, None, block)  

    def parse_assignment_or_expression(self):
        identifier = self.parse_identifier()
        if self.current_token[0] == 'ASSIGN':  # Si es una asignación (=>)
            self.advance()  # Avanzamos el token de asignación (=>)
            expression = self.parse_expression()
            self.expect('SEMICOLON')  # Ahora se espera el punto y coma al final
            return BinaryOpNode(identifier, 'ASSIGN', expression)
        else:
            raise SyntaxError(f"Token inesperado {self.current_token[0]}")

    def parse_declaration(self):
        self.expect('HUNTER')
        identifier_list = self.parse_identifier_list()
        self.expect('COLON')
        var_type = self.current_token[0]
        self.advance()
        expression = None
        if self.current_token[0] == 'ASSIGN':
            self.advance()
            expression = self.parse_expression()
        self.expect('SEMICOLON')  # Asegurar que la declaración también termina con un ;
        return DeclarationNode(identifier_list, var_type, expression)

    def parse_identifier_list(self):
        identifiers = [self.parse_identifier()]
        while self.current_token[0] == 'COMMA':
            self.advance()
            identifiers.append(self.parse_identifier())
        return identifiers

    def parse_if_statement(self):
        self.expect('INSIGHT')
        self.expect('LPAREN')
        condition = self.parse_expression()
        self.expect('RPAREN')
        true_block = self.parse_block()
        false_block = None
        if self.current_token[0] == 'MADNESS':
            self.advance()
            false_block = self.parse_block()
        return IfStatementNode(condition, true_block, false_block)

    def parse_nightmare_loop(self):
        self.expect('NIGHTMARE')
        self.expect('LPAREN')
        init = self.parse_expression()
        self.expect('SEMICOLON')
        condition = self.parse_expression()
        self.expect('SEMICOLON')
        increment = self.parse_expression()
        self.expect('RPAREN')
        block = self.parse_block()
        return LoopNode(init, condition, increment, block)

    def parse_pray(self):
        self.expect('PRAY')
        self.expect('LPAREN')
        expression = self.parse_expression()  
        self.expect('RPAREN')
        self.expect('SEMICOLON')
        return FunctionCallNode('PRAY', [expression])

    def parse_rest_statement(self):
        self.expect('REST')
        self.expect('SEMICOLON')
        return RestNode()

    def parse_expression(self):
        left = self.parse_term()
        while self.current_token[0] in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EQUAL', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL', 'NOT', 'BLOODBOND', 'OLDBLOOD']:
            operator = self.current_token[0]
            self.advance()
            right = self.parse_term()
            left = BinaryOpNode(left, operator, right)
        return left  # Eliminamos el punto y coma aquí, porque no siempre es necesario.

    def parse_term(self):
        if self.current_token[0] == 'NUMBER':
            value = self.current_token[1]
            self.advance()
            return NumberNode(value)
        elif self.current_token[0] == 'STRING':
            value = self.current_token[1]
            self.advance()
            return StringNode(value)
        elif self.current_token[0] == 'IDENTIFIER':
            return self.parse_identifier()
        elif self.current_token[0] == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            self.expect('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Token inesperado {self.current_token[0]}")

    def parse_identifier(self):
        name = self.current_token[1]
        self.advance()
        return IdentifierNode(name)
