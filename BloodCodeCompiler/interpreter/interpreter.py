from parser.ast import ASTNode, NumberNode, IdentifierNode, BinaryOpNode, StringNode, DeclarationNode, BlockNode, IfStatementNode, LoopNode, FunctionCallNode, RestNode, BooleanNode, UnaryOpNode, FunctionDeclarationNode, ReturnNode, ArrayNode

class Interpreter:
    def __init__(self, env):
        self.env = env
        self.context = {}
        self.functions = {}
        self.output = [] 
        self.prompt_var = None

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
                RestNode: lambda _: None,  # RestNode no ejecuta nada
                ArrayNode: self.execute_array,
                ReturnNode: self.execute_return,
            }

            # Ejecutar la función asociada con el tipo de nodo
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
        return self.context.get(node.name, None)

    def execute_function_call(self, node):
        try:
            if node.identifier == 'PRAY':
                return self._handle_pray(node)
            elif node.identifier == 'EYES':
                return self._handle_eyes(node)
            elif node.identifier.name in self.functions:
                return self._execute_user_defined_function(node)
            raise Exception(f"Función no encontrada: {node.identifier.name}")
        except Exception as e:
            raise Exception(f"Error en la línea {node.line_number}: {str(e)}")

    def _handle_pray(self, node):
        full_message = "".join(str(self.execute(expr)) for expr in node.arguments)
        self.output.append(full_message)
        return None

    def _handle_eyes(self, node):
        for var in node.arguments:
            var_type = self.env.get_variable_type(var.name)
            if 'input_var' in self.context:
                value = self._convert_input_value(var_type, self.context['input_var'], var.name)
                self.context[var.name] = value
                del self.context['input_var']
            else:
                self.prompt_var = f"Ingrese valor para la variable {var.name}"
                return None
        return None


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
        func = self.functions[node.identifier.name]
        local_context = self.context.copy()

        for param, arg in zip(func.parameters, node.arguments):
            local_context[param[0].name] = self.execute(arg)

        return self.execute_block_with_context(func.block, local_context)

    def execute_block_with_context(self, block, context):
        previous_context = self.context
        self.context = context

        for statement in block.statements:
            result = self.execute(statement)
            if isinstance(statement, ReturnNode):
                break

        self.context = previous_context
        return result

    def execute_return(self, node):
        return self.execute(node.expression)

    def execute_block(self, node):
        for statement in node.statements:
            self.execute(statement)  

            if isinstance(statement, FunctionCallNode) and statement.identifier == 'PRAY':
                continue 

            if isinstance(statement, ReturnNode):
                return self.execute(statement.expression)  

        return None

    def execute_array(self, node):
        return [self.execute(element) for element in node.elements]

    def execute_declaration(self, node):
        for identifier in node.identifier_list:
            value = None
            if isinstance(node.var_type, tuple):  # Manejo de arrays
                value = self._initialize_array(node, identifier)
            elif node.expression: 
                value = self.execute(node.expression)
            self.context[identifier.name] = value 
        return None


    def _initialize_array(self, node, identifier):
        element_type, size = node.var_type
        size_value = self.execute(size)

        if isinstance(node.expression, ArrayNode):  
            array_value = self.execute(node.expression)
            if len(array_value) != size_value:
                raise Exception(f"Tamaño del vector {identifier.name} no coincide con la inicialización")
            return array_value
        else:
            return [None] * size_value 

    
    def execute_function_declaration(self, node):
        self.functions[node.name.name] = node 
        return None

    def execute_binary_op(self, node):
        try:
            left_value = self.execute(node.left)
            right_value = self.execute(node.right)
            if node.operator == 'INDEX':
                return self._execute_index_op(node, left_value, right_value)
            if node.operator in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE']:
                return self._execute_arithmetic_op(node.operator, left_value, right_value)
            if node.operator == 'ASSIGN':
                return self._execute_assign_op(node, left_value, right_value)
            if node.operator in ['EQUAL', 'NOT', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL']:
                return self._execute_comparison_op(node.operator, left_value, right_value)
            if node.operator in ['BLOODBOND', 'OLDBLOOD', 'VILEBLOOD']:
                return self._execute_logical_op(node.operator, left_value, right_value)
            raise Exception(f"Operador no soportado: {node.operator}")
        except Exception as e:
            raise Exception(f"Error en la línea {node.line_number}: {str(e)}")

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

    def _execute_assign_op(self, node, left_value, right_value):
        if isinstance(node.left, BinaryOpNode) and node.left.operator == 'INDEX':
            array = self.context.get(node.left.left.name)
            if array is None:
                raise Exception(f"Variable no definida: {node.left.left.name}")
            index = self.execute(node.left.right)
            value = self.execute(node.right)
            array[index] = value
            return value
        elif isinstance(node.left, IdentifierNode):
            value = self.execute(node.right)
            self.context[node.left.name] = value
            return value
        raise Exception(f"Error en asignación: nodo no soportado")

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
        if operator == 'BLOODBOND':  # AND
            return left_value and right_value
        elif operator == 'OLDBLOOD':  # OR
            return left_value or right_value
        elif operator == 'VILEBLOOD':  # NOT
            return not right_value
        raise Exception(f"Operador lógico no soportado: {operator}")

    def _execute_index_op(self, node, left_value, right_value):
        array = self.context.get(node.left.name)
        if array is None:
            raise Exception(f"Variable no definida: {node.left.name}")
        index = self.execute(node.right)
        return array[index]

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
        if node.init:
            self.execute(node.init)

        while self.execute(node.condition):
            self.execute(node.block)
            if node.increment:
                self.execute(node.increment)
        return None