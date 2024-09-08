from ..parser.ast import ASTNode, NumberNode, IdentifierNode, BinaryOpNode, StringNode, DeclarationNode, BlockNode, IfStatementNode, LoopNode, FunctionCallNode, RestNode,BooleanNode, UnaryOpNode, FunctionDeclarationNode, ReturnNode, ArrayNode


class Interpreter:
    def __init__(self, env):
        self.env = env
        self.context = {}  # Contexto global
        self.functions = {}  # Diccionario para almacenar funciones

    def execute(self, node):
        if isinstance(node, BlockNode):
            return self.execute_block(node)
        elif isinstance(node, DeclarationNode):
            return self.execute_declaration(node)
        elif isinstance(node, BinaryOpNode):
            return self.execute_binary_op(node)
        elif isinstance(node, NumberNode):
            return int(node.value) if node.value.isdigit() else float(node.value)
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
            return self.execute_array(node)  # Ejecutamos el nuevo ArrayNode
        elif isinstance(node, ReturnNode):
            return self.execute_return(node)
        else:
            raise Exception(f"Nodo no soportado: {type(node)}")

    def execute_function_declaration(self, node):
        # Guardamos la función en el diccionario de funciones
        self.functions[node.name.name] = node

    def execute_function_call(self, node):
        # Buscamos la función en el diccionario
        func = self.functions.get(node.identifier.name)
        if func is None:
            raise Exception(f"Función no encontrada: {node.identifier.name}")

        # Crear un nuevo contexto local para los parámetros de la función
        local_context = self.context.copy()

        # Evaluar y asignar los argumentos a los parámetros
        for param, arg in zip(func.parameters, node.arguments):
            local_context[param[0].name] = self.execute(arg)

        # Ejecutar el cuerpo de la función con el contexto local
        result = self.execute_block_with_context(func.block, local_context)

        # Asegurar que se devuelve el resultado correcto
        return result

    def execute_block_with_context(self, block, context):
        # Guardar el contexto anterior y establecer el nuevo
        previous_context = self.context
        self.context = context

        result = None
        for statement in block.statements:
            result = self.execute(statement)
            if isinstance(statement, ReturnNode):
                break  # Devolver inmediatamente si hay un return

        # Restaurar el contexto anterior después de ejecutar el bloque
        self.context = previous_context
        return result

    def execute_return(self, node):
        # Evaluar la expresión de retorno y devolver su valor
        return self.execute(node.expression)

    def execute_block(self, node):
        result = None
        for statement in node.statements:
            result = self.execute(statement)
            if isinstance(statement, ReturnNode):
                return result  # Salir inmediatamente si se encuentra un return
        return result

    def execute_array(self, node):
        # Evaluamos cada elemento del vector y los almacenamos en una lista de Python
        return [self.execute(element) for element in node.elements]

    def execute_declaration(self, node):
        for identifier in node.identifier_list:
            value = None
            if isinstance(node.var_type, tuple):  # Si el tipo es un vector (ejemplo: Maria[10])
                element_type, size = node.var_type
                size_value = self.execute(size)  # Evaluamos el tamaño del vector

                if isinstance(node.expression, ArrayNode):  # Si la inicialización es un ArrayNode
                    value = self.execute(node.expression)  # Evaluamos el ArrayNode
                    if len(value) != size_value:  # Verificamos que el tamaño coincida
                        raise Exception(f"Tamaño del vector {identifier.name} no coincide con la inicialización")
                else:
                    value = [None] * size_value  # Inicializamos con `None` si no hay valores iniciales
            elif node.expression:
                value = self.execute(node.expression)

            self.context[identifier.name] = value  # Guardamos la variable o vector en el contexto
        return None

    def execute_binary_op(self, node):
        left_value = self.execute(node.left)
        right_value = self.execute(node.right)

        # Convertir cadenas numéricas a números para evitar concatenación indebida
        if isinstance(left_value, str) and left_value.isdigit():
            left_value = int(left_value)
        if isinstance(right_value, str) and right_value.isdigit():
            right_value = int(right_value)

        if node.operator == 'INDEX':  # Acceso a un elemento del vector
            array = self.context.get(node.left.name)
            if array is None:
                raise Exception(f"Variable no definida: {node.left.name}")
            index = self.execute(node.right)
            return array[index]  # Devolvemos el valor en el índice especificado
        
        # Operaciones aritméticas y de concatenación
        if node.operator == 'PLUS':
            if isinstance(left_value, (int, float)) and isinstance(right_value, (int, float)):
                return left_value + right_value
            elif isinstance(left_value, str) and isinstance(right_value, str):
                return left_value + right_value  # Concatenación si ambos son cadenas
            else:
                raise Exception(f"Error de tipos: No se puede sumar {type(left_value)} y {type(right_value)}")
        elif node.operator == 'MINUS':
            return left_value - right_value
        elif node.operator == 'MULTIPLY':
            return left_value * right_value
        elif node.operator == 'DIVIDE':
            if right_value == 0:
                raise ValueError("División por cero")
            return left_value / right_value

        # Asignación
        elif node.operator == 'ASSIGN':
            if isinstance(node.left, BinaryOpNode) and node.left.operator == 'INDEX':  # Asignación a un elemento del vector
                array = self.context.get(node.left.left.name)
                if array is None:
                    raise Exception(f"Variable no definida: {node.left.left.name}")
                index = self.execute(node.left.right)
                value = self.execute(node.right)
                array[index] = value  # Asignamos el valor en el índice especificado
                return value

            elif isinstance(node.left, IdentifierNode):
                value = self.execute(node.right)
                self.context[node.left.name] = value  # Asignamos el valor a la variable
                return value

        # Operadores de comparación
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

        # Operadores lógicos
        elif node.operator == 'BLOODBOND':  # AND lógico (&&)
            return left_value and right_value
        elif node.operator == 'OLDBLOOD':  # OR lógico (||)
            return left_value or right_value
        elif node.operator == 'VILEBLOOD':  # NOT lógico (!)
            return not self.execute(node.right)

        else:
            raise Exception(f"Operador no soportado: {node.operator}")

    def execute_unary_op(self, node):
        operand_value = self.execute(node.operand)
        if node.operator == 'VILEBLOOD':  # Negación lógica
            return not operand_value
        else:
            raise Exception(f"Operador unario no soportado: {node.operator}")
            
    def execute_if_statement(self, node):
        condition_value = self.execute(node.condition)
        if condition_value:
            return self.execute(node.true_block)
        elif node.false_block:
            return self.execute(node.false_block)
        return None

    def execute_loop(self, node):
        # Verificamos si el bucle es del tipo "NIGHTMARE" (con init, condition, increment) o "DREAM" (solo condition)
        if node.init:
            self.execute(node.init)  # Ejecutamos la inicialización solo si existe (para NIGHTMARE)
        
        while self.execute(node.condition):  # Evaluamos la condición
            self.execute(node.block)  # Ejecutamos el bloque
            if node.increment:
                self.execute(node.increment)  # Incremento solo si existe (para NIGHTMARE)
        
        return None

    def execute_function_call(self, node):
        # Manejar la función especial PRAY
        if node.identifier == 'PRAY':
            for expr in node.arguments:
                result = self.execute(expr)
                print(result)  # Imprimir la expresión evaluada
            return None  # PRAY no tiene valor de retorno
        
        elif node.identifier == 'EYES':
            for var in node.arguments:
                var_type = self.env.get_variable_type(var.name)
                value = input(f"Ingrese valor para {var.name}: ")
                
                # Validar el tipo de la variable y convertir el valor ingresado
                if var_type == 'MARIA':  # Número
                    try:
                        value = int(value)  # Convertir el valor ingresado a entero
                    except ValueError:
                        raise Exception(f"Error: Se esperaba un valor numérico para '{var.name}'")
                elif var_type == 'EILEEN':  # Cadena
                    value = str(value)
                else:
                    raise Exception(f"Tipo no soportado para 'Eyes': {var_type}")
                
                self.context[var.name] = value  # Guardar el valor en el contexto
            return None
            
        # Manejar otras funciones
        func = self.functions.get(node.identifier.name)
        if func is None:
            raise Exception(f"Función no encontrada: {node.identifier.name}")

        # Crear un nuevo contexto local para los parámetros de la función
        local_context = self.context.copy()

        # Evaluar y asignar los argumentos a los parámetros
        for param, arg in zip(func.parameters, node.arguments):
            local_context[param[0].name] = self.execute(arg)

        # Ejecutar el cuerpo de la función con el contexto local
        result = self.execute_block_with_context(func.block, local_context)

        return result