from ..parser.ast import ASTNode, NumberNode, IdentifierNode, BinaryOpNode, StringNode, DeclarationNode, BlockNode, IfStatementNode, LoopNode, FunctionCallNode, RestNode, BooleanNode, UnaryOpNode

class Interpreter:
    def __init__(self):
        self.context = {}

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
        elif isinstance(node, RestNode):
            return None
        else:
            raise Exception(f"Nodo no soportado: {type(node)}")

    def execute_block(self, node):
        result = None
        for statement in node.statements:
            result = self.execute(statement)
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
            return left_value + right_value
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
        if node.identifier == 'EYES':
            prompt = self.execute(node.arguments[0]) 
            return input(prompt)
        elif node.identifier == 'PRAY':
            for expr in node.arguments:
                result = self.execute(expr)
                print(result)
        else:
            raise Exception(f"Función no soportada: {node.identifier}")

    def run(self, ast):
        return self.execute(ast)
