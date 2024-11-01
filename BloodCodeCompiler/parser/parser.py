from .ast import ASTNode, NumberNode, IdentifierNode, BinaryOpNode, StringNode, DeclarationNode, BlockNode, IfStatementNode, LoopNode, FunctionCallNode, RestNode, BooleanNode, UnaryOpNode, FunctionDeclarationNode, ReturnNode, ArrayNode
from lexer.lexer import Token
def error_handler(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            raise SyntaxError(f"Error en {func.__name__}: {str(e)} ")
    return wrapper

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.token_position = 0
        self.current_token = self.tokens[self.token_position]

    def check_token_type(self, token_type):
        if self.current_token.type != token_type:
            raise SyntaxError(f"Se esperaba {token_type}, pero se encontró {self.current_token.type} en la línea {self.current_token.line_number}")

    def consume_token(self):
        self.token_position += 1
        if self.token_position < len(self.tokens):
            self.current_token = self.tokens[self.token_position]

    def validate_and_consume_token(self, token_type):
        self.check_token_type(token_type)
        self.consume_token()

    @error_handler
    def parse(self):
        return self.parse_main_block()

    @error_handler
    def parse_block(self):
        statements = []
        self.validate_and_consume_token('LBRACE')
        while self.current_token.type != 'RBRACE':
            if self.token_position >= len(self.tokens):  
                raise SyntaxError(f"Bloque no cerrado correctamente en la línea {self.current_token.line_number}")
            statements.append(self.parse_statement())
        self.validate_and_consume_token('RBRACE')
        return BlockNode(statements, self.current_token.line_number)
    
    @error_handler
    def parse_statement(self):
        parse_map = {
            'HUNTER': self.parse_declaration,
            'GREATONES': self.parse_function_declaration,
            'ECHOES': self.parse_return_statement,
            'INSIGHT': self.parse_if_statement,
            'NIGHTMARE': self.parse_nightmare_loop,
            'DREAM': self.parse_dream_loop,
            'PRAY': self.parse_pray,
            'EYES': self.parse_eyes_statement,
            'REST': self.parse_rest_statement,
            'IDENTIFIER': self.parse_assignment_or_expression
        }
        parse_func = parse_map.get(self.current_token.type)
        if parse_func:
            return parse_func()
        else:
            return self.parse_expression()
        
    @error_handler
    def parse_declaration(self):
        self.validate_and_consume_token('HUNTER')
        identifier_list = self.parse_identifier_list()
        self.validate_and_consume_token('COLON')

        var_type = self.current_token.type
        self.consume_token()

        if self.current_token.type == 'LBRACKET':
            self.consume_token()
            if self.current_token.type == 'RBRACKET':
                self.consume_token()
                var_type = (var_type, None)
            else:  
                size = self.parse_expression()
                self.validate_and_consume_token('RBRACKET')
                var_type = (var_type, size)

        expression = None
        if self.current_token.type == 'ASSIGN':
            self.consume_token()
            if self.current_token.type == 'LBRACKET':
                expression = self.parse_array()
            else:
                expression = self.parse_expression()

        self.validate_and_consume_token('SEMICOLON')
        return DeclarationNode(identifier_list, var_type, expression, self.current_token.line_number)

    @error_handler
    def parse_identifier_list(self):
        identifiers = [self.parse_identifier()] 
        while self.current_token.type == 'COMMA':  
            self.consume_token()  
            identifiers.append(self.parse_identifier())  
        return identifiers

    @error_handler
    def parse_identifier(self):
        self.check_token_type('IDENTIFIER')
        name = self.current_token.value
        line_number = self.current_token.line_number
        self.consume_token()
        return IdentifierNode(name, line_number)
        
    @error_handler
    def parse_function_declaration(self):
        self.validate_and_consume_token('GREATONES')  
        func_name = self.parse_identifier()  

        self.validate_and_consume_token('LPAREN') 

        params = []
        if self.current_token.type != 'RPAREN': 
            params = self.parse_parameter_list()  
        self.validate_and_consume_token('RPAREN')  

        self.validate_and_consume_token('COLON') 
        return_type = self.current_token.value 
        line_number = self.current_token.line_number
        self.consume_token()  

        block = self.parse_block() 
        return FunctionDeclarationNode(func_name, params, return_type, block, line_number)

    @error_handler
    def parse_parameter_list(self):
        params = [self.parse_parameter()]
        while self.current_token.type == 'COMMA':
            self.consume_token()
            params.append(self.parse_parameter())
        return params

    def parse_parameter(self):
        param_name = self.parse_identifier() 
        self.validate_and_consume_token('COLON') 
        param_type = self.current_token.value 
        self.consume_token() 
        return (param_name, param_type)

    def parse_return_statement(self):
        self.validate_and_consume_token('ECHOES')  
        expression = self.parse_expression()  
        self.validate_and_consume_token('SEMICOLON')  
        return ReturnNode(expression, self.current_token.line_number)

    def parse_eyes_statement(self):
        self.validate_and_consume_token('EYES')   
        self.validate_and_consume_token('LPAREN')
        identifier = self.parse_identifier() 
        self.validate_and_consume_token('RPAREN')
        self.validate_and_consume_token('SEMICOLON') 
        return FunctionCallNode('EYES', [identifier], self.current_token.line_number)

    def parse_dream_loop(self):
        self.validate_and_consume_token('DREAM')
        self.validate_and_consume_token('LPAREN')
        condition = self.parse_expression()
        self.validate_and_consume_token('RPAREN')
        block = self.parse_block()  
        return LoopNode(None, condition, None, block, self.current_token.line_number)

    @error_handler
    def parse_assignment_or_expression(self):
        identifier = self.parse_identifier()

        if self.current_token.type == 'LBRACKET': 
            return self.parse_array_assignment_or_access(identifier)
        elif self.current_token.type == 'ASSIGN': 
            return self.parse_assignment(identifier)
        else:
            return self.parse_expression()
        
    @error_handler
    def parse_array_assignment_or_access(self, identifier):
        self.consume_token()  
        index = self.parse_expression()  
        self.validate_and_consume_token('RBRACKET')

        if self.current_token.type == 'ASSIGN':
            self.consume_token()  
            expression = self.parse_expression()  
            self.validate_and_consume_token('SEMICOLON')
            return BinaryOpNode(BinaryOpNode(identifier, 'INDEX', index, self.current_token.line_number), 'ASSIGN', expression, self.current_token.line_number)
        
        return BinaryOpNode(identifier, 'INDEX', index, self.current_token.line_number)

    @error_handler
    def parse_function_call(self, identifier):
        self.consume_token()  
        arguments = []
        if self.current_token.type != 'RPAREN':  
            arguments = self.parse_argument_list()  
        self.validate_and_consume_token('RPAREN')
        self.validate_and_consume_token('SEMICOLON')
        
        return FunctionCallNode(identifier, arguments, self.current_token.line_number)

    @error_handler
    def parse_assignment(self, identifier):
        self.consume_token()
        
        if self.current_token.type == 'EYES':
            expression = self.parse_eyes()
        else:
            expression = self.parse_expression()
        
        self.validate_and_consume_token('SEMICOLON')
        
        return BinaryOpNode(identifier, 'ASSIGN', expression, self.current_token.line_number)

    def parse_if_statement(self):
        self.validate_and_consume_token('INSIGHT')
        self.validate_and_consume_token('LPAREN')
        condition = self.parse_expression()
        self.validate_and_consume_token('RPAREN')
        true_block = self.parse_block()
        false_block = None
        if self.current_token.type == 'MADNESS':
            self.consume_token()
            false_block = self.parse_block()
        return IfStatementNode(condition, true_block, false_block, self.current_token.line_number)

    def parse_nightmare_loop(self):
        self.validate_and_consume_token('NIGHTMARE')
        self.validate_and_consume_token('LPAREN')
        if self.current_token.type == 'HUNTER':
            init = self.parse_declaration()  
        else:
            init = self.parse_assignment_or_expression()  

        condition = self.parse_expression()
        self.validate_and_consume_token('SEMICOLON')

        increment = self.parse_assignment_or_expression()
        self.validate_and_consume_token('RPAREN')

        block = self.parse_block()

        return LoopNode(init, condition, increment, block, self.current_token.line_number)

    def parse_pray(self):
        self.validate_and_consume_token('PRAY')
        self.validate_and_consume_token('LPAREN')
        expression = self.parse_expression()  
        self.validate_and_consume_token('RPAREN')
        self.validate_and_consume_token('SEMICOLON')
        return FunctionCallNode('PRAY', [expression], self.current_token.line_number)

    def parse_rest_statement(self):
        self.validate_and_consume_token('REST')
        self.validate_and_consume_token('SEMICOLON')
        return RestNode(self.current_token.line_number)

    def parse_expression(self):
        if self.current_token.type == 'LBRACKET': 
            self.consume_token()  
            elements = []
            while self.current_token.type != 'RBRACKET':
                elements.append(self.parse_expression()) 
                if self.current_token.type == 'COMMA':
                    self.consume_token() 
            self.validate_and_consume_token('RBRACKET')  
            return ArrayNode(elements, self.current_token.line_number)
        return self.parse_logical_or()

    def parse_binary_operation(self, parse_lower_precedence, operators):
        node = parse_lower_precedence()
        while self.current_token.type in operators:
            operator = self.current_token.type
            self.consume_token()
            right = parse_lower_precedence()
            node = BinaryOpNode(node, operator, right, self.current_token.line_number)
        return node

    def parse_logical_or(self):
        return self.parse_binary_operation(self.parse_logical_and, {'OLDBLOOD'})

    def parse_logical_and(self):
        return self.parse_binary_operation(self.parse_equality, {'BLOODBOND'})

    def parse_equality(self):
        return self.parse_binary_operation(self.parse_relational, {'EQUAL', 'NOT'})

    def parse_relational(self):
        return self.parse_binary_operation(self.parse_additive, {'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL'})

    def parse_additive(self):
        return self.parse_binary_operation(self.parse_multiplicative, {'PLUS', 'MINUS'})

    def parse_multiplicative(self):
        return self.parse_binary_operation(self.parse_unary, {'MULTIPLY', 'DIVIDE'})

    def parse_unary(self):
        if self.current_token.type == 'VILEBLOOD':
            operator = self.current_token.type
            self.consume_token()
            operand = self.parse_unary()
            return UnaryOpNode(operator, operand, self.current_token.line_number)
        else:
            return self.parse_primary()


    @error_handler
    def parse_primary(self):
        if self.current_token.type == 'NUMBER':
            return self.parse_number()

        elif self.current_token.type == 'STRING':
            return self.parse_string()

        elif self.current_token.type in ('TRUE', 'FALSE'):
            return self.parse_boolean()

        elif self.current_token.type == 'IDENTIFIER':
            return self.parse_identifier_expression()

        elif self.current_token.type == 'LPAREN':
            self.consume_token()
            expr = self.parse_expression()
            self.validate_and_consume_token('RPAREN')
            return expr

        else:
            raise SyntaxError(f"Token inesperado {self.current_token.type} en la línea {self.current_token.line_number} --> {self.current_token.value}")

    def parse_number(self):
        value = self.current_token.value
        line_number = self.current_token.line_number
        self.consume_token()
        return NumberNode(float(value), line_number)

    def parse_string(self):
        value = self.current_token.value
        line_number = self.current_token.line_number
        self.consume_token()
        return StringNode(value, line_number)

    def parse_boolean(self):
        line_number = self.current_token.line_number
        value = True if self.current_token.type == 'TRUE' else False
        self.consume_token()
        return BooleanNode(value, line_number)

    def parse_identifier_expression(self):
        identifier = self.parse_identifier()
        if self.current_token.type == 'LBRACKET':
            return self.parse_array_access(identifier)
        elif self.current_token.type == 'LPAREN':
            return self.parse_function_call(identifier)
        return identifier

    def parse_array_access(self, identifier):
        self.consume_token()
        index = self.parse_expression()
        self.validate_and_consume_token('RBRACKET')
        return BinaryOpNode(identifier, 'INDEX', index, self.current_token.line_number)

    def parse_function_call(self, identifier):
        self.consume_token()
        arguments = []
        if self.current_token.type != 'RPAREN':
            arguments = self.parse_argument_list()
        self.validate_and_consume_token('RPAREN')
        return FunctionCallNode(identifier, arguments, self.current_token.line_number)


    def parse_argument_list(self):
        arguments = [self.parse_expression()] 
        while self.current_token.type == 'COMMA':  
            self.consume_token()
            arguments.append(self.parse_expression())
        return arguments

    def parse_identifier(self):
        name = self.current_token.value
        line_number = self.current_token.line_number
        self.consume_token()
        return IdentifierNode(name, line_number)

    def parse_main_block(self):
        statements = []
        while self.token_position < len(self.tokens): 
            statements.append(self.parse_statement()) 
        return BlockNode(statements, self.current_token.line_number)

    def parse_eyes(self):
        self.validate_and_consume_token('EYES')
        self.validate_and_consume_token('LPAREN')  
        prompt = self.parse_expression()  
        self.validate_and_consume_token('RPAREN') 
        return FunctionCallNode('EYES', [prompt], self.current_token.line_number)
    
    @error_handler
    def parse_array(self):
        elements = []
        self.validate_and_consume_token('LBRACKET')  
        while self.current_token.type != 'RBRACKET':
            elements.append(self.parse_expression())  
            if self.current_token.type == 'COMMA':
                self.consume_token()  
        self.validate_and_consume_token('RBRACKET')
        return ArrayNode(elements, self.current_token.line_number)

