from parser.ast import ASTNode, NumberNode, IdentifierNode, BinaryOpNode, StringNode, DeclarationNode, BlockNode, IfStatementNode, LoopNode, FunctionCallNode, RestNode, BooleanNode, UnaryOpNode, FunctionDeclarationNode, ReturnNode, ArrayNode

class Interpreter:
    def __init__(self, env):
        self.env = env
        self.context = {}
        self.functions = {}
        self.output = []
        self.prompt_var = None
        self.pending_input_var = None

    def execute(self, node):
        try:
            node_type_to_function = {
                BlockNode: self.execute_block,
                DeclarationNode: self.execute_declaration,
                BinaryOpNode: self.execute_binary_op,
                NumberNode: self.execute_number,
                StringNode: self.execute_string,
                BooleanNode: self.execute_boolean,
                IdentifierNode: self.execute_identifier,
                IfStatementNode: self.execute_if_statement,
                LoopNode: self.execute_loop,
                FunctionCallNode: self.execute_function_call,
                UnaryOpNode: self.execute_unary_op,
                FunctionDeclarationNode: self.execute_function_declaration,
                RestNode: lambda _: None,
                ArrayNode: self.execute_array,
                ReturnNode: self.execute_return,
            }

            execute_func = node_type_to_function.get(type(node))
            if execute_func:
                return execute_func(node)
            else:
                raise Exception(f"Nodo no soportado: {type(node)}")

        except Exception as e:
            raise Exception(f"Error en la línea {node.line_number}: {str(e)}")

    def execute_number(self, node):
        if float(node.value).is_integer():
            return int(node.value)
        return float(node.value)

    def execute_string(self, node):
        return node.value

    def execute_boolean(self, node):
        return node.value

    def execute_identifier(self, node):
        if node.name not in self.context:
            raise Exception(f"Error: La variable '{node.name}' no ha sido inicializada.")
        value = self.context[node.name]
        
        if value is None:
            raise Exception(f"Error: La variable '{node.name}' fue declarada pero no ha sido inicializada.")
        
        return value

    def execute_function_call(self, node):
        if isinstance(node.identifier, IdentifierNode):
            function_name = node.identifier.name
        else:
            function_name = node.identifier

        if function_name == 'PRAY':
            full_message = "".join(str(self.execute(expr)) for expr in node.arguments)
            self.output.append(full_message)
            return None

        elif function_name == 'EYES':
            for var in node.arguments:
                var_name = var.name if isinstance(var, IdentifierNode) else var
                var_type = self.env.get_variable_type(var_name)
                
                if 'input_var' in self.context: 
                    value = self.context['input_var']
                    if isinstance(var_type, tuple): 
                        element_type = var_type[0]
                        if element_type == 'MARIA':
                            value = [int(v) for v in value.split()] 
                        elif element_type == 'EILEEN':
                            value = value.split()
                        else:
                            raise Exception(f"Tipo no soportado para 'Eyes': {element_type}")
                    else:
                        if var_type == 'MARIA':
                            value = int(value)
                        elif var_type == 'EILEEN':
                            value = str(value)
                        else:
                            raise Exception(f"Tipo no soportado para 'Eyes': {var_type}")
                    
                    self.context[var_name] = value 
                    del self.context['input_var']
                    self.pending_input_var = None 
                else:
                    self.prompt_var = f"Ingrese valor para la variable {var_name}"
                    self.pending_input_var = var_name
                    return None

        if function_name in self.functions:
            func = self.functions[function_name]
            local_context = self.context.copy()
            for param, arg in zip(func.parameters, node.arguments):
                local_context[param[0].name] = self.execute(arg)
            result = self.execute_block_with_context(func.block, local_context)
            return result

    def _convert_input_value(self, var_type, value, var_name):
        try:
            if var_type == 'MARIA':  
                return int(value)
            elif var_type == 'EILEEN':  
                return str(value)
            else:
                raise Exception(f"Tipo no soportado para 'Eyes': {var_type}")
        except ValueError:
            raise Exception(f"Error: Se esperaba un valor numérico para '{var_name}'")

    def _execute_user_defined_function(self, node):
        func = self.functions.get(node.identifier.name)
        if func is None:
            raise Exception(f"Función '{node.identifier.name}' no encontrada.")
        local_context = self.context.copy()

        for param, arg in zip(func.parameters, node.arguments):
            local_context[param[0].name] = self.execute(arg)

        return self.execute_block_with_context(func.block, local_context)

    def execute_block_with_context(self, block, context):
        previous_context = self.context
        self.context = context

        try:
            result = None
            for statement in block.statements:
                result = self.execute(statement)
                if isinstance(statement, ReturnNode):
                    return result
        finally:
            self.context = previous_context
        return result

    def execute_return(self, node):
        return self.execute(node.expression)

    def execute_block(self, node):
        result = None
        for statement in node.statements:
            result = self.execute(statement)
            if isinstance(statement, ReturnNode):
                return result
        return result

    def execute_array(self, node):
        return [self.execute(element) for element in node.elements]

    def execute_declaration(self, node):
        for identifier in node.identifier_list:
            value = None

            if isinstance(node.var_type, tuple):
                element_type = node.var_type[0]
                size1 = self.execute(node.var_type[1]) if node.var_type[1] else 0

                if len(node.var_type) == 2:
                    if isinstance(node.expression, ArrayNode):
                        init_value = self.execute(node.expression)
                        if len(init_value) != size1:
                            raise Exception(f"Tamaño del array '{identifier.name}' no coincide con la inicialización.")
                        value = init_value
                    else:
                        value = [0] * size1 if element_type == 'MARIA' else [""] * size1

                elif len(node.var_type) == 3:
                    size2 = self.execute(node.var_type[2]) if node.var_type[2] else 0
                    value = [[0] * size2 for _ in range(size1)] if element_type == 'MARIA' else [[""] * size2 for _ in range(size1)]

                    if isinstance(node.expression, ArrayNode):
                        init_value = self.execute(node.expression)
                        if len(init_value) != size1:
                            raise Exception(f"Tamaño de la matriz '{identifier.name}' no coincide con la inicialización.")
                        for i, row in enumerate(init_value):
                            if len(row) != size2:
                                raise Exception(f"Tamaño de fila {i} en la matriz '{identifier.name}' no coincide con la inicialización.")
                        value = init_value

            elif node.expression:
                value = self.execute(node.expression)
            else:
                value = "" if node.var_type == 'EILEEN' else 0
            self.context[identifier.name] = value
        return None

    def _get_base_identifier_name(self, node):
        current_node = node
        while isinstance(current_node, BinaryOpNode) and current_node.operator == 'INDEX':
            current_node = current_node.left
        if isinstance(current_node, IdentifierNode):
            return current_node.name
        else:
            raise Exception("Acceso de matriz inválido: falta el identificador base.")

    def execute_binary_op(self, node):
        if node.operator == 'ASSIGN':
            right_value = self.execute(node.right)

            if isinstance(node.left, IdentifierNode):
                self.context[node.left.name] = right_value
                return right_value

            elif isinstance(node.left, BinaryOpNode) and node.left.operator == 'INDEX':
                base_name = self._get_base_identifier_name(node.left)
                array = self.context.get(base_name)
                if array is None:
                    raise Exception(f"Variable no definida: {base_name}")

                if isinstance(array[0], list):  
                    row_index = self.execute(node.left.left.right)
                    col_index = self.execute(node.left.right)
                    if not (0 <= row_index < len(array)) or not (0 <= col_index < len(array[0])):
                        raise Exception(f"Índice fuera de rango en la matriz '{base_name}'")
                    array[row_index][col_index] = right_value

                else:  
                    index = self.execute(node.left.right)
                    if not (0 <= index < len(array)):
                        raise Exception(f"Índice fuera de rango en el vector '{base_name}'")
                    array[index] = right_value

                return right_value

        elif node.operator == 'INDEX':
            base_name = self._get_base_identifier_name(node.left)
            array = self.context.get(base_name)
            if array is None:
                raise Exception(f"Variable no definida: {base_name}")

            if isinstance(array[0], list):  
                row_index = self.execute(node.left.right)
                col_index = self.execute(node.right)
                if not (0 <= row_index < len(array)) or not (0 <= col_index < len(array[0])):
                    raise Exception(f"Índice fuera de rango en la matriz '{base_name}'")
                return array[row_index][col_index]

            else:  
                index = self.execute(node.right)
                if not (0 <= index < len(array)):
                    raise Exception(f"Índice fuera de rango en el vector '{base_name}'")
                return array[index]

        left_value = self.execute(node.left)
        right_value = self.execute(node.right)
        if node.operator in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE']:
            return self._execute_arithmetic_op(node.operator, left_value, right_value)
        if node.operator in ['EQUAL', 'NOT', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL']:
            return self._execute_comparison_op(node.operator, left_value, right_value)
        if node.operator in ['BLOODBOND', 'OLDBLOOD', 'VILEBLOOD']:
            return self._execute_logical_op(node.operator, left_value, right_value)

        raise Exception(f"Operador no soportado: {node.operator}")

    def _execute_arithmetic_op(self, operator, left_value, right_value):
        if operator == 'PLUS':
            return left_value + right_value
        elif operator == 'MINUS':
            return left_value - right_value
        elif operator == 'MULTIPLY':
            return left_value * right_value
        elif operator == 'DIVIDE':
            return left_value / right_value
        raise Exception(f"Operador aritmético no soportado: {operator}")

    def _execute_comparison_op(self, operator, left_value, right_value):
        if operator == 'EQUAL':
            return left_value == right_value
        elif operator == 'NOT':
            return left_value != right_value
        elif operator == 'GREATER':
            return left_value > right_value
        elif operator == 'LESS':
            return left_value < right_value
        elif operator == 'GREATEREQUAL':
            return left_value >= right_value
        elif operator == 'LESSEQUAL':
            return left_value <= right_value
        raise Exception(f"Operador comparativo no soportado: {operator}")

    def _execute_logical_op(self, operator, left_value, right_value):
        if operator == 'BLOODBOND':  
            return left_value and right_value
        elif operator == 'OLDBLOOD':  
            return left_value or right_value
        elif operator == 'VILEBLOOD': 
            return not right_value
        raise Exception(f"Operador lógico no soportado: {operator}")

    def execute_unary_op(self, node):
        operand_value = self.execute(node.operand)
        if node.operator == 'VILEBLOOD':
            return not operand_value
        else:
            raise Exception(f"Operador unario no soportado: {node.operator}")

    def execute_if_statement(self, node):
        condition_value = self.execute(node.condition)
        if condition_value:
            self.execute(node.true_block)
        elif node.false_block:
            self.execute(node.false_block)

    def execute_loop(self, node):
        if isinstance(node.init, DeclarationNode):
            self.execute_declaration(node.init)
        elif node.init:
            self.execute(node.init) 

        while self.execute(node.condition):
            self.execute(node.block) 

            if node.increment:
                self.execute(node.increment) 

    def execute_function_declaration(self, node):
            self.functions[node.name.name] = node 
            return None