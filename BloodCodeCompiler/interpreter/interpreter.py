from ..parser.ast import ASTNode, NumberNode, IdentifierNode, BinaryOpNode, StringNode, DeclarationNode, BlockNode, IfStatementNode, LoopNode, FunctionCallNode, RestNode
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
        elif isinstance(node, IdentifierNode):
            return self.context.get(node.name, None)
        elif isinstance(node, IfStatementNode):
            return self.execute_if_statement(node)
        elif isinstance(node, LoopNode):
            return self.execute_loop(node)
        elif isinstance(node, FunctionCallNode):
            return self.execute_function_call(node)
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

        if node.operator == 'PLUS':
            return left_value + right_value
        elif node.operator == 'MINUS':
            return left_value - right_value
        elif node.operator == 'MULTIPLY':
            return left_value * right_value
        elif node.operator == 'DIVIDE':
            return left_value / right_value

        elif node.operator == 'ASSIGN':
            if isinstance(node.left, IdentifierNode):
                self.context[node.left.name] = right_value
                return right_value
            else:
                raise Exception("Asignación no válida")

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
        self.execute(node.init)  # Inicialización
        while self.execute(node.condition):  # Condición
            self.execute(node.block)  # Cuerpo del bucle
            self.execute(node.increment)  # Incremento
        return None

    def execute_function_call(self, node):
        if node.identifier == 'PRAY':
            for expr in node.arguments:
                result = self.execute(expr)
                print(result)  # Imprimir la expresión evaluada
        else:
            raise Exception(f"Función no soportada: {node.identifier}")
