from ..parser.ast import ASTNode, NumberNode, IdentifierNode, BinaryOpNode, StringNode, DeclarationNode, BlockNode, IfStatementNode, LoopNode, FunctionCallNode, RestNode, FunctionDeclarationNode, ReturnNode, ArrayNode

class SemanticError(Exception): 
    def __init__(self, message, node=None):
        self.message = message
        self.node = node
        super().__init__(self._format_message())

    def _format_message(self):
        if self.node:
            return f"Error semántico: {self.message} en el nodo {type(self.node).__name__}"
        else:
            return f"Error semántico: {self.message}"


class SemanticAnalyzer:
    def __init__(self, env):
        self.env = env

    def analyze(self, node):
        if isinstance(node, BlockNode):
            self.analyze_block(node)
        elif isinstance(node, DeclarationNode):
            self.analyze_declaration(node)
        elif isinstance(node, BinaryOpNode):
            return self.analyze_binary_op(node)
        elif isinstance(node, NumberNode):
            return 'MARIA' 
        elif isinstance(node, StringNode):
            return 'EILEEN' 
        elif isinstance(node, IdentifierNode):
            return self.env.get_variable_type(node.name)
        elif isinstance(node, ArrayNode):
            return self.analyze_array(node)
        elif isinstance(node, FunctionCallNode):
            return self.analyze_function_call(node)
        elif isinstance(node, IfStatementNode):
            self.analyze_if_statement(node)
        elif isinstance(node, LoopNode):
            self.analyze_loop(node)
        elif isinstance(node, FunctionDeclarationNode):
            self.analyze_function_declaration(node)
        elif isinstance(node, ReturnNode):
            return self.analyze_return(node)
        else:
            raise SemanticError(f"Nodo no soportado: {type(node)}", node)

    def analyze_block(self, node):
        for statement in node.statements:
            self.analyze(statement)

    def analyze_declaration(self, node):
        var_type = node.var_type
        for identifier in node.identifier_list:
            self.env.declare_variable(identifier.name, var_type)
        if node.expression:
            expr_type = self.analyze(node.expression)
            if isinstance(var_type, tuple):  
                if expr_type != 'ARRAY':
                    raise SemanticError(f"Se esperaba un array para la variable '{identifier.name}', pero se encontró {expr_type}", node)
            else:
                if expr_type != var_type:
                    raise SemanticError(f"Error de tipo: Se esperaba '{var_type}' para la variable '{identifier.name}', pero se encontró '{expr_type}'", node)

    def analyze_binary_op(self, node):
        left_type = self.analyze(node.left)
        right_type = self.analyze(node.right)
        
        if node.operator in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE']:
            if left_type != 'MARIA' or right_type != 'MARIA':
                raise SemanticError(f"Operación aritmética requiere ambos operandos de tipo 'MARIA', pero se encontró '{left_type}' y '{right_type}'", node)
            return 'MARIA'

        elif node.operator == 'ASSIGN':
            if isinstance(node.left, BinaryOpNode) and node.left.operator == 'INDEX':
                array_type = self.analyze(node.left.left)
                if not isinstance(array_type, tuple) or array_type[0] != 'MARIA':
                    raise SemanticError(f"El acceso a índices solo es válido para arrays de 'MARIA', pero se encontró '{array_type}'", node)
                index_type = self.analyze(node.left.right)
                if index_type != 'MARIA':
                    raise SemanticError(f"Los índices de arrays deben ser de tipo 'MARIA', pero se encontró '{index_type}'", node)
                if right_type != 'MARIA':
                    raise SemanticError(f"Solo se pueden asignar valores de tipo 'MARIA' a un array de 'MARIA', pero se encontró '{right_type}'", node)
                return array_type[0]
            if left_type != right_type:
                raise SemanticError(f"No se puede asignar un valor de tipo '{right_type}' a '{left_type}'", node)
            return left_type

        elif node.operator == 'INDEX':
            array_type = self.analyze(node.left)
            if not isinstance(array_type, tuple):
                raise SemanticError(f"{node.left.name} no es un array", node)
            index_type = self.analyze(node.right)
            if index_type != 'MARIA':
                raise SemanticError(f"El índice debe ser de tipo 'MARIA', pero se encontró '{index_type}'", node)
            return array_type[0]

        elif node.operator in ['EQUAL', 'NOT', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL']:
            if left_type != right_type:
                raise SemanticError(f"Los operandos de una comparación deben ser del mismo tipo, pero se encontró '{left_type}' y '{right_type}'", node)
            return 'BLOOD'  

        elif node.operator in ['BLOODBOND', 'OLDBLOOD', 'VILEBLOOD']:
            if left_type != 'BLOOD' or right_type != 'BLOOD':
                raise SemanticError(f"Los operadores lógicos requieren valores booleanos de tipo 'BLOOD', pero se encontró '{left_type}' y '{right_type}'", node)
            return 'BLOOD'
        
        else:
            raise SemanticError(f"Operador no soportado: {node.operator}", node)

    def analyze_array(self, node):
        element_type = None
        for element in node.elements:
            elem_type = self.analyze(element)
            if element_type is None:
                element_type = elem_type
            elif elem_type != element_type:
                raise Exception(f"Error de tipo: Todos los elementos del array deben ser del mismo tipo, pero se encontró {elem_type}")
        return 'ARRAY'  

    def analyze_function_call(self, node):
        if node.identifier in ['PRAY', 'EYES']:
            if len(node.arguments) != 1:
                raise SemanticError(f"La función '{node.identifier}' espera 1 argumento, pero se encontraron {len(node.arguments)}", node)
            
            arg_type = self.analyze(node.arguments[0])
            if node.identifier == 'PRAY' and arg_type not in ['MARIA', 'EILEEN']: 
                raise SemanticError(f"La función 'PRAY' solo puede imprimir valores de tipo 'MARIA' o 'EILEEN', pero se encontró '{arg_type}'", node)
            elif node.identifier == 'EYES' and arg_type not in ['MARIA', 'EILEEN']: 
                raise SemanticError(f"La función 'EYES' solo puede leer valores de tipo 'MARIA' o 'EILEEN', pero se encontró '{arg_type}'", node)

            return None  

        func_type = self.env.get_function_type(node.identifier.name)
        param_types, return_type = func_type

        if len(node.arguments) != len(param_types):
            raise SemanticError(f"Error de tipo: La función '{node.identifier.name}' espera {len(param_types)} argumentos, pero se encontraron {len(node.arguments)}", node)

        for i, arg in enumerate(node.arguments):
            arg_type = self.analyze(arg)
            if arg_type != param_types[i]:
                raise SemanticError(f"Error de tipo: Argumento {i+1} de la función '{node.identifier.name}' esperaba {param_types[i]}, pero se encontró {arg_type}", node)

        return return_type

    def analyze_if_statement(self, node):
        condition_type = self.analyze(node.condition)
        if condition_type != 'BLOOD':
            raise Exception(f"Error de tipo: La condición en un 'if' debe ser de tipo 'BLOOD'")
        self.analyze(node.true_block)
        if node.false_block:
            self.analyze(node.false_block)

    def analyze_loop(self, node):
        condition_type = self.analyze(node.condition)
        if condition_type != 'BLOOD':
            raise Exception(f"Error de tipo: La condición en un bucle debe ser de tipo 'BLOOD'")
        self.analyze(node.block)

    def analyze_function_declaration(self, node):
        param_types = [param_type for _, param_type in node.parameters]
        return_type = node.return_type

        self.env.declare_function(node.name.name, param_types, return_type)

        self.env.enter_scope()

        for param_name, param_type in node.parameters:
            self.env.declare_variable(param_name.name, param_type)

        self.analyze(node.block)

        if return_type != 'ROM':  
            if not self.has_return(node.block):
                raise Exception(f"Error: La función '{node.name.name}' debe tener una instrucción de retorno de tipo {return_type}")

        self.env.exit_scope()

    def has_return(self, block_node):
        for statement in block_node.statements:
            if isinstance(statement, ReturnNode):
                return True
            elif isinstance(statement, IfStatementNode):
                return self.has_return(statement.true_block) and (statement.false_block is None or self.has_return(statement.false_block))
            elif isinstance(statement, BlockNode):
                if self.has_return(statement):
                    return True
        return False

    def analyze_return(self, node):
        return_type = self.analyze(node.expression)
        return return_type