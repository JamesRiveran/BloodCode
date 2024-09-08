from .ast import ASTNode, NumberNode, IdentifierNode, BinaryOpNode, StringNode, DeclarationNode, BlockNode, IfStatementNode, LoopNode, FunctionCallNode, RestNode, FunctionDeclarationNode, ReturnNode, ArrayNode

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

        # Verificar si es un acceso a un vector (ejemplo: abc[1])
        if self.current_token[0] == 'LBRACKET':
            self.advance()  # Consumimos el '['
            index = self.parse_expression()  # Parseamos el índice
            self.expect('RBRACKET')  # Consumimos el ']'
            if self.current_token[0] == 'ASSIGN':  # Si es una asignación (=>)
                self.advance()  # Consumimos el '=>'
                expression = self.parse_expression()
                self.expect('SEMICOLON')  # Esperamos el punto y coma al final
                return BinaryOpNode(BinaryOpNode(identifier, 'INDEX', index), 'ASSIGN', expression)
            else:
                return BinaryOpNode(identifier, 'INDEX', index)

        elif self.current_token[0] == 'ASSIGN':  # Si es una asignación a una variable normal
            self.advance()  # Consumimos el '=>'
            expression = self.parse_expression()
            self.expect('SEMICOLON')  # Ahora se espera el punto y coma al final
            return BinaryOpNode(identifier, 'ASSIGN', expression)
        else:
            raise SyntaxError(f"Token inesperado {self.current_token[0]}")



    def parse_declaration(self):
        self.expect('HUNTER')
        identifier_list = self.parse_identifier_list()
        self.expect('COLON')

        # Verificar si el tipo es un vector (ejemplo: Maria[10])
        var_type = self.current_token[0]
        self.advance()

        if self.current_token[0] == 'LBRACKET':  # Si es un array (ejemplo: Maria[10])
            self.advance()  # Consumimos el '['
            size = self.parse_expression()  # Parseamos el tamaño del vector (ej. 10)
            self.expect('RBRACKET')  # Consumimos el ']'
            var_type = (var_type, size)  # Guardamos el tipo y el tamaño del vector

        expression = None
        if self.current_token[0] == 'ASSIGN':
            self.advance()
            expression = self.parse_expression()  # Parseamos la expresión que inicializa el vector
        self.expect('SEMICOLON')  # Aseguramos que la declaración termina con un punto y coma
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
        if self.current_token[0] == 'LBRACKET':  # Si encontramos un corchete, es una lista (vector)
            self.advance()  # Consumimos el '['
            elements = []
            while self.current_token[0] != 'RBRACKET':
                elements.append(self.parse_expression())  # Parseamos cada elemento de la lista
                if self.current_token[0] == 'COMMA':
                    self.advance()  # Consumimos la coma entre los elementos
            self.expect('RBRACKET')  # Consumimos el ']'
            return ArrayNode(elements)  # Devolvemos un ArrayNode en lugar de una lista de Python

        # El resto del código de `parse_expression` maneja números, operadores, identificadores, etc.
        left = self.parse_term()
        while self.current_token[0] in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'EQUAL', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL', 'NOT', 'BLOODBOND', 'OLDBLOOD']:
            operator = self.current_token[0]
            self.advance()
            right = self.parse_term()
            left = BinaryOpNode(left, operator, right)
        return left



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

            # Verificar si es un acceso a un vector (ejemplo: cba[0])
            if self.current_token[0] == 'LBRACKET':
                self.advance()  # Consumimos el '['
                index = self.parse_expression()  # Parseamos el índice
                self.expect('RBRACKET')  # Consumimos el ']'
                return BinaryOpNode(identifier, 'INDEX', index)  # Nodo para el acceso al vector

            # Verificar si es una llamada a función
            elif self.current_token[0] == 'LPAREN':
                self.advance()  # Consumir el '('
                arguments = []
                if self.current_token[0] != 'RPAREN':
                    arguments = self.parse_argument_list()
                self.expect('RPAREN')
                return FunctionCallNode(identifier, arguments)

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
