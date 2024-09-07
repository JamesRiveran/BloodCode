from .ast import ASTNode, NumberNode, IdentifierNode, BinaryOpNode, StringNode, DeclarationNode, BlockNode, IfStatementNode, LoopNode, FunctionCallNode, RestNode, FunctionDeclarationNode, ReturnNode

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
        elif self.current_token[0] == 'GREATONES':
            return self.parse_function_declaration()
        elif self.current_token[0] == 'ECHOES': 
            return self.parse_return_statement()
        elif self.current_token[0] == 'INSIGHT':
            return self.parse_if_statement()
        elif self.current_token[0] == 'NIGHTMARE':
            return self.parse_nightmare_loop()
        elif self.current_token[0] == 'DREAM':
            return self.parse_dream_loop()  
        elif self.current_token[0] == 'PRAY':
            return self.parse_pray()
        elif self.current_token[0] == 'EYES':
            return self.parse_eyes_statement()
        elif self.current_token[0] == 'REST':
            return self.parse_rest_statement()
        elif self.current_token[0] == 'IDENTIFIER': 
            return self.parse_assignment_or_expression()
        else:
            return self.parse_expression()

    def parse_function_declaration(self):
        self.expect('GREATONES')  # Reconocemos la palabra clave para la función
        func_name = self.parse_identifier()  # Obtenemos el nombre de la función
        self.expect('LPAREN')  # Abrimos paréntesis para los parámetros

        # Parseamos los parámetros de la función
        params = []
        if self.current_token[0] != 'RPAREN':
            params = self.parse_parameter_list()
        self.expect('RPAREN')  # Cerramos paréntesis de los parámetros

        self.expect('COLON')  # Esperamos el tipo de retorno
        return_type = self.current_token[0]
        self.advance()

        # Parseamos el cuerpo de la función
        block = self.parse_block()

        return FunctionDeclarationNode(func_name, params, return_type, block)

    def parse_parameter_list(self):
        params = []
        params.append(self.parse_parameter())
        while self.current_token[0] == 'COMMA':
            self.advance()
            params.append(self.parse_parameter())
        return params

    def parse_parameter(self):
        param_name = self.parse_identifier()
        self.expect('COLON')
        param_type = self.current_token[0]
        self.advance()
        return (param_name, param_type)

    def parse_return_statement(self):
        self.expect('ECHOES')  # Reconocer la palabra clave 'echoes'
        expression = self.parse_expression()  # Parsear la expresión que sigue al 'echoes'
        self.expect('SEMICOLON')  # Esperar el punto y coma al final
        return ReturnNode(expression)  # Devolver un nodo de retorno

    def parse_eyes_statement(self):
        self.expect('EYES')  # Reconocemos el token 'EYES'
        self.expect('LPAREN')
        identifier = self.parse_identifier() 
        self.expect('RPAREN')
        self.expect('SEMICOLON')  # Se espera un punto y coma al final
        return FunctionCallNode('EYES', [identifier])  

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
        elif self.current_token[0] == 'LPAREN':  # Si es una llamada a función
            self.advance()  # Consumir el '('
            arguments = []
            if self.current_token[0] != 'RPAREN':  # Si no es ')', parsear los argumentos
                arguments = self.parse_argument_list()
            self.expect('RPAREN')  # Consumir el ')'
            self.expect('SEMICOLON')
            return FunctionCallNode(identifier, arguments)
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
        if self.current_token[0] == 'HUNTER':
            init = self.parse_declaration()  
        else:
            init = self.parse_assignment_or_expression()  


        condition = self.parse_expression()
        self.expect('SEMICOLON')

        increment = self.parse_assignment_or_expression()
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
            identifier = self.parse_identifier()
            
            # Verificar si es una llamada a función
            if self.current_token[0] == 'LPAREN':
                self.advance()  # Consumir el '('
                arguments = []
                if self.current_token[0] != 'RPAREN':  # Si no es ')', parsear los argumentos
                    arguments = self.parse_argument_list()
                self.expect('RPAREN')  # Consumir el ')'
                return FunctionCallNode(identifier, arguments)  # Retornar el nodo de llamada a función
            else:
                return identifier
        elif self.current_token[0] == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            self.expect('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Token inesperado {self.current_token[0]}")


        
    def parse_argument_list(self):
        arguments = [self.parse_expression()]  # Parsear el primer argumento
        while self.current_token[0] == 'COMMA':  # Parsear el resto de los argumentos
            self.advance()
            arguments.append(self.parse_expression())
        return arguments


    def parse_identifier(self):
        name = self.current_token[1]
        self.advance()
        return IdentifierNode(name)
