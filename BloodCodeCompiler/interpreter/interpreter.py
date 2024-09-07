from ..parser.ast import ASTNode, NumberNode, IdentifierNode, BinaryOpNode, StringNode, DeclarationNode, BlockNode, IfStatementNode, LoopNode, FunctionCallNode, RestNode, FunctionDeclarationNode, ReturnNode

class Interpreter:
    def __init__(self):
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
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, IdentifierNode):
            return self.context.get(node.name, None)
        elif isinstance(node, IfStatementNode):
            return self.execute_if_statement(node)
        elif isinstance(node, LoopNode):
            return self.execute_loop(node)
        elif isinstance(node, FunctionCallNode):
            return self.execute_function_call(node)
        elif isinstance(node, FunctionDeclarationNode):
            return self.execute_function_declaration(node)
        elif isinstance(node, RestNode):
            return None
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

    def execute_declaration(self, node):
        for identifier in node.identifier_list:
            value = None
            if node.expression:
                value = self.execute(node.expression)
            self.context[identifier.name] = value
        return None

    def execute_binary_op(self, node):
        left_value = self.execute(node.left)
        right_value = self.execute(node.right)

        # Convertir cadenas numéricas a números para evitar concatenación indebida
        if isinstance(left_value, str) and left_value.isdigit():
            left_value = int(left_value)
        if isinstance(right_value, str) and right_value.isdigit():
            right_value = int(right_value)

        # Operaciones aritméticas y de concatenación
        if node.operator == 'PLUS':
            if isinstance(left_value, (int, float)) and isinstance(right_value, (int, float)):
                return left_value + right_value
            elif isinstance(left_value, str) and isinstance(right_value, str):
                return left_value + right_value  # Concatenación si ambos son cadenas
            else:
                raise Exception(f"Error de tipos: No se puede sumar {type(left_value)} y {type(right_value)}")
        
        elif node.operator == 'MINUS':
            if isinstance(left_value, (int, float)) and isinstance(right_value, (int, float)):
                return left_value - right_value
            else:
                raise Exception(f"Error de tipos: No se puede restar {type(left_value)} y {type(right_value)}")
        
        elif node.operator == 'MULTIPLY':
            if isinstance(left_value, (int, float)) and isinstance(right_value, (int, float)):
                return left_value * right_value
            else:
                raise Exception(f"Error de tipos: No se puede multiplicar {type(left_value)} y {type(right_value)}")
        
        elif node.operator == 'DIVIDE':
            if isinstance(left_value, (int, float)) and isinstance(right_value, (int, float)):
                return left_value / right_value
            else:
                raise Exception(f"Error de tipos: No se puede dividir {type(left_value)} y {type(right_value)}")
        
        # Asignación
        elif node.operator == 'ASSIGN':
            if isinstance(node.left, IdentifierNode):
                self.context[node.left.name] = right_value
                return right_value
            else:
                raise Exception("Asignación no válida")

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
            return not left_value

        else:
            raise Exception(f"Operador no soportado: {node.operator}")

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
                value = input(f"Ingrese valor para {var.name}: ")  # Pedir entrada al usuario
                self.context[var.name] = value
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
