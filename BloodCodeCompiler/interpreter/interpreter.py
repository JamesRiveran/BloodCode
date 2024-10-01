from ..parser.ast import ASTNode, NumberNode, IdentifierNode, BinaryOpNode, StringNode, DeclarationNode, BlockNode, IfStatementNode, LoopNode, FunctionCallNode, RestNode, BooleanNode, UnaryOpNode, FunctionDeclarationNode, ReturnNode, ArrayNode

class Interpreter:
    def __init__(self, env):
        self.env = env
        self.context = {}
        self.functions = {}
        self.output = [] 

    def execute(self, node):
        if isinstance(node, BlockNode):
            return self.execute_block(node)
        elif isinstance(node, DeclarationNode):
            return self.execute_declaration(node)
        elif isinstance(node, BinaryOpNode):
            return self.execute_binary_op(node)
        if isinstance(node, NumberNode):
            if float(node.value).is_integer():
                return int(node.value)  
            else:
                return float(node.value)
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, BooleanNode):
            return node.value
        elif isinstance(node, IdentifierNode):
            return self.context.get(node.name, None)
        elif isinstance(node, IfStatementNode):
            return self.execute_if_statement(node)
        elif isinstance(node, LoopNode):
            return self.execute_loop(node)
        elif isinstance(node, FunctionCallNode):
            return self.execute_function_call(node)
        elif isinstance(node, UnaryOpNode):
            return self.execute_unary_op(node)
        elif isinstance(node, FunctionDeclarationNode):
            return self.execute_function_declaration(node)
        elif isinstance(node, RestNode):
            return None
        elif isinstance(node, ArrayNode):
            return self.execute_array(node)
        elif isinstance(node, ReturnNode):
            return self.execute_return(node)
        else:
            raise Exception(f"Nodo no soportado: {type(node)}")

    def execute_function_call(self, node):
        if node.identifier == 'PRAY':
            full_message = ""  
            for expr in node.arguments:
                result = self.execute(expr)
                full_message += str(result)
            self.output.append(full_message)
            return None

        elif node.identifier == 'EYES':
            for var in node.arguments:
                var_type = self.env.get_variable_type(var.name)
                value = input(f"Ingrese valor para {var.name}: ")
                
                if var_type == 'MARIA':  
                    try:
                        value = int(value)
                    except ValueError:
                        raise Exception(f"Error: Se esperaba un valor numérico para '{var.name}'")
                elif var_type == 'EILEEN':  
                    value = str(value)
                else:
                    raise Exception(f"Tipo no soportado para 'Eyes': {var_type}")
                
                self.context[var.name] = value  
            return None

        if node.identifier.name in self.functions:
            func = self.functions[node.identifier.name]  

            local_context = self.context.copy()

            for param, arg in zip(func.parameters, node.arguments):
                local_context[param[0].name] = self.execute(arg)

            result = self.execute_block_with_context(func.block, local_context)
            return result

        raise Exception(f"Función no encontrada: {node.identifier.name}")


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
            if isinstance(node.var_type, tuple):
                element_type, size = node.var_type
                size_value = self.execute(size)

                if isinstance(node.expression, ArrayNode):
                    value = self.execute(node.expression)
                    if len(value) != size_value:
                        raise Exception(f"Tamaño del vector {identifier.name} no coincide con la inicialización")
                else:
                    value = [None] * size_value
            elif node.expression:
                value = self.execute(node.expression)

            self.context[identifier.name] = value
        return None
    
    def execute_function_declaration(self, node):
        self.functions[node.name.name] = node 
        return None

    def execute_binary_op(self, node):
        left_value = self.execute(node.left)
        right_value = self.execute(node.right)

        if isinstance(left_value, str) and left_value.isdigit():
            left_value = int(left_value)
        if isinstance(right_value, str) and right_value.isdigit():
            right_value = int(right_value)

        if node.operator == 'INDEX':
            array = self.context.get(node.left.name)
            if array is None:
                raise Exception(f"Variable no definida: {node.left.name}")
            index = self.execute(node.right)
            return array[index]

        if node.operator == 'PLUS':
            return left_value + right_value
        elif node.operator == 'MINUS':
            return left_value - right_value
        elif node.operator == 'MULTIPLY':
            return left_value * right_value
        elif node.operator == 'DIVIDE':
            return left_value / right_value

        elif node.operator == 'ASSIGN':
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

        elif node.operator == 'EQUAL':
            return left_value == right_value
        elif node.operator == 'NOT':
            return left_value != right_value
        elif node.operator == 'GREATER':
            return left_value > right_value
        elif node.operator == 'LESS':
            return left_value < right_value
        elif node.operator == 'GREATEREQUAL':
            return left_value >= right_value
        elif node.operator == 'LESSEQUAL':
            return left_value <= right_value

        elif node.operator == 'BLOODBOND':
            return left_value and right_value
        elif node.operator == 'OLDBLOOD':
            return left_value or right_value
        elif node.operator == 'VILEBLOOD':
            return not self.execute(node.right)

        else:
            raise Exception(f"Operador no soportado: {node.operator}")

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