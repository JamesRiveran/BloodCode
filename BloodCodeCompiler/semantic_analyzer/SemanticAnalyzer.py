from parser.ast import ASTNode, NumberNode, IdentifierNode, BinaryOpNode, StringNode, DeclarationNode, BlockNode, IfStatementNode, LoopNode, FunctionCallNode, RestNode, BooleanNode, UnaryOpNode, FunctionDeclarationNode, ReturnNode, ArrayNode

class SemanticError(Exception):
    def __init__(self, message, node=None):
        self.message = message
        self.node = node
        self.line_number = getattr(node, 'line_number', 'desconocida') 
        super().__init__(self._format_message())

    def _format_message(self):
        node_info = f" en el nodo {type(self.node).__name__}" if self.node else ""
        line_info = f" en la línea {self.line_number}" if self.line_number != 'desconocida' else ""
        return f"Error semántico: {self.message}{node_info}{line_info}"


def semantic_error_handler(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except SemanticError as e:
            raise SyntaxError(f"Error en {func.__name__}: {str(e)}")
        except Exception as e:
            raise SyntaxError(f"Error inesperado en {func.__name__}: {str(e)}")
    return wrapper


class SemanticAnalyzer:
    def __init__(self, env):
        self.env = env

    @semantic_error_handler
    def analyze(self, node):
        node_type_to_method = {
            BlockNode: self.analyze_block,
            DeclarationNode: self.analyze_declaration,
            BinaryOpNode: self.analyze_binary_op,
            NumberNode: self.analyze_number,
            StringNode: self.analyze_string,
            IdentifierNode: self.analyze_identifier,
            ArrayNode: self.analyze_array,
            FunctionCallNode: self.analyze_function_call,
            IfStatementNode: self.analyze_if_statement,
            LoopNode: self.analyze_loop,
            FunctionDeclarationNode: self.analyze_function_declaration,
            ReturnNode: self.analyze_return,
            BooleanNode: self.analyze_boolean,
            UnaryOpNode: self.analyze_unary_op,
        }
        
        analyze_method = node_type_to_method.get(type(node))
        if analyze_method:
            return analyze_method(node)
        else:
            raise SemanticError(f"Nodo no soportado: {type(node)}", node)

    def analyze_number(self, node):
        if float(node.value).is_integer():
            return 'MARIA'
        return 'GEHRMAN'


    def analyze_string(self, node):
        return 'EILEEN'

    def analyze_identifier(self, node):
        return self.env.get_variable_type(node.name)

    def analyze_boolean(self, node):
        return 'BLOOD'

    @semantic_error_handler
    def analyze_block(self, node):
        for statement in node.statements:
            self.analyze(statement)

    def analyze_declaration(self, node):
        var_type = node.var_type
        if isinstance(var_type, tuple):
            element_type = var_type[0].upper()

            if len(var_type) == 3:
                size1 = var_type[1]
                size2 = var_type[2]
                if size1:
                    self._validate_array_size(size1, node.identifier_list[0], node)
                if size2:
                    self._validate_array_size(size2, node.identifier_list[0], node)
                array_type = (element_type, 'MATRIX')
            
            elif len(var_type) == 2:
                size_expr = var_type[1]
                if size_expr:
                    self._validate_array_size(size_expr, node.identifier_list[0], node)
                array_type = (element_type, 'ARRAY')
        else:
            array_type = var_type.upper()

        for identifier in node.identifier_list:
            self.env.declare_variable(identifier.name, array_type)

        if node.expression:
            expr_type = self.analyze(node.expression)
            if isinstance(var_type, tuple):
                if len(var_type) == 3:
                    self._validate_matrix_declaration(var_type, expr_type, identifier, node)
                else:
                    self._validate_array_declaration(var_type, expr_type, identifier, node)
            else:
                self._validate_type_match(array_type, expr_type.upper(), identifier, node)

    def _validate_matrix_declaration(self, var_type, expr_type, identifier, node):
        element_type = var_type[0].upper()

        if expr_type != 'MATRIX':
            raise SemanticError(f"Se esperaba una matriz para la variable '{identifier.name}', pero se encontró {expr_type}", node)

        if isinstance(node.expression, ArrayNode):
            for row in node.expression.elements:
                if not isinstance(row, ArrayNode):
                    raise SemanticError(f"Se esperaba una matriz 2D para '{identifier.name}'", node)
                for element in row.elements:
                    element_type_from_expr = self.analyze(element).upper()
                    if element_type_from_expr != element_type:
                        raise SemanticError(f"Todos los elementos de la matriz '{identifier.name}' deben ser de tipo '{element_type}', pero se encontró {element_type_from_expr}", node)
        return 'MATRIX'

    def _validate_array_size(self, size, identifier, node):
        size_type = self.analyze(size)
        if size_type != 'MARIA':  
            raise SemanticError(f"El tamaño del array '{identifier.name}' debe ser de tipo 'MARIA', pero se encontró '{size_type}'", node)

    def _validate_array_declaration(self, var_type, expr_type, identifier, node):
        element_type = var_type[0].upper() 

        if expr_type != 'ARRAY':
            raise SemanticError(f"Se esperaba un array para la variable '{identifier.name}', pero se encontró {expr_type}", node)

        if isinstance(node.expression, ArrayNode):
            for element in node.expression.elements:
                element_type_from_expr = self.analyze(element).upper()
                print(f"Declarando array {identifier.name}, tipo esperado: {element_type}, tipo encontrado: {element_type_from_expr}")

                if element_type_from_expr != element_type:
                    raise SemanticError(f"Todos los elementos del array '{identifier.name}' deben ser de tipo '{element_type}', pero se encontró {element_type_from_expr}", node)

        return 'ARRAY'

    def _validate_type_match(self, var_type, expr_type, identifier, node):
        if self.normalize_type(expr_type) != self.normalize_type(var_type):
            raise SemanticError(f"Error de tipo: Se esperaba '{var_type}' para la variable '{identifier.name}', pero se encontró '{expr_type}'", node)

    @semantic_error_handler
    def analyze_binary_op(self, node):
        if node.operator == 'INDEX':
            return self._analyze_index_op(node)

        left_type = self.analyze(node.left)
        right_type = self.analyze(node.right)

        if node.operator in ['ASSIGN', 'ARROW_ASSIGN']:
            if isinstance(node.left, IdentifierNode):
                left_type = self.analyze(node.left)
                right_type = self.analyze(node.right)
                if left_type != right_type:
                    raise SemanticError(f"No se puede asignar un valor de tipo '{right_type}' a '{left_type}'", node)
                return left_type

            elif isinstance(node.left, BinaryOpNode) and node.left.operator == 'INDEX':
                base_identifier_name = self._get_base_identifier_name(node.left)
                try:
                    array_type = self.env.get_variable_type(base_identifier_name)
                except Exception as e:
                    raise SemanticError(str(e), node)

                if not isinstance(array_type, tuple) or array_type[1] not in ['ARRAY', 'MATRIX']:
                    raise SemanticError(f"Acceso inválido: '{base_identifier_name}' no es un array o matriz", node)

                element_type = array_type[0]
                if element_type != right_type:
                    raise SemanticError(f"No se puede asignar '{right_type}' a un '{element_type}' en el array o matriz", node)

                return element_type

        elif node.operator in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE']:
            return self._analyze_arithmetic_op(left_type, right_type, node)

        elif node.operator in ['EQUAL', 'NOT', 'GREATER', 'LESS', 'GREATEREQUAL', 'LESSEQUAL']:
            return self._analyze_comparison_op(left_type, right_type, node)

        elif node.operator in ['BLOODBOND', 'OLDBLOOD', 'VILEBLOOD']:
            return self._analyze_logical_op(left_type, right_type, node)

        raise SemanticError(f"Operador no soportado: {node.operator}", node)


    def _analyze_index_op(self, node):
        base_identifier_name = self._get_base_identifier_name(node.left)
        array_type = self.env.get_variable_type(base_identifier_name)

        if not isinstance(array_type, tuple):
            raise SemanticError(f"{base_identifier_name} no es un array o matriz", node)

        index_type = self.analyze(node.right)
        if index_type != 'MARIA':
            raise SemanticError(f"Índice debe ser de tipo 'MARIA', pero se encontró '{index_type}'", node)

        return array_type[0]

    def _get_base_identifier_name(self, node):
        current_node = node
        while isinstance(current_node, BinaryOpNode) and current_node.operator == 'INDEX':
            current_node = current_node.left
        if isinstance(current_node, IdentifierNode):
            return current_node.name
        else:
            raise SemanticError("Estructura de acceso inválida: falta identificador base en matriz o array.", node)

    def _analyze_arithmetic_op(self, left_type, right_type, node):
        left_type = self.normalize_type(left_type)
        right_type = self.normalize_type(right_type)
        if left_type == 'MARIA' and right_type == 'MARIA':
            return 'MARIA'
        elif left_type == 'EILEEN' and right_type == 'EILEEN':
            return 'EILEEN'
        else:
            raise SemanticError(
                f"Operación aritmética requiere ambos operandos de tipo 'MARIA' o ambos de tipo 'EILEEN', "
                f"pero se encontró '{left_type}' y '{right_type}'",
                node
            )

    def _analyze_assignment_op(self, node, left_type, right_type):
        if isinstance(node.left, BinaryOpNode) and node.left.operator == 'INDEX':
            array_type = self.analyze(node.left.left)

            if not isinstance(array_type, tuple) or array_type[1] not in ['ARRAY', 'MATRIX']:
                raise SemanticError(f"Acceso inválido: {node.left.left.name} no es un array o matriz", node)

            element_type = array_type[0]
            if element_type != right_type:
                raise SemanticError(f"No se puede asignar '{right_type}' a un '{element_type}' en el array o matriz", node)

            index_type = self.analyze(node.left.right)
            if index_type != 'MARIA':
                raise SemanticError(f"Índice del array/matriz debe ser 'MARIA', no '{index_type}'", node)

            if isinstance(node.left.left, BinaryOpNode) and node.left.left.operator == 'INDEX':
                col_index_type = self.analyze(node.left.left.right)
                if col_index_type != 'MARIA':
                    raise SemanticError(f"Índice de columna debe ser 'MARIA', no '{col_index_type}'", node)

            return element_type


    def _analyze_comparison_op(self, left_type, right_type, node):
        left_type = self.normalize_type(left_type)
        right_type = self.normalize_type(right_type)
        if left_type != right_type:
            raise SemanticError(f"Los operandos de una comparación deben ser del mismo tipo, pero se encontró '{left_type}' y '{right_type}'", node)
        return 'BLOOD'
 

    def _analyze_logical_op(self, left_type, right_type, node):
        left_type = self.normalize_type(left_type)
        right_type = self.normalize_type(right_type)
        if left_type != 'BLOOD' or right_type != 'BLOOD':
            raise SemanticError(f"Los operadores lógicos requieren valores booleanos de tipo 'BLOOD', pero se encontró '{left_type}' y '{right_type}'", node)
        return 'BLOOD'


    @semantic_error_handler
    def analyze_array(self, node):
        element_type = None
        for element in node.elements:
            elem_type = self.analyze(element)
            if element_type is None:
                element_type = elem_type
            elif elem_type != element_type:
                raise SemanticError(f"Error de tipo: Todos los elementos del array deben ser del mismo tipo, pero se encontró {elem_type}")
        return 'ARRAY'  

    def _analyze_builtin_function_call(self, node):
        if len(node.arguments) != 1:
            raise SemanticError(f"La función '{node.identifier}' espera 1 argumento, pero se encontraron {len(node.arguments)}", node)
        
        arg_type = self.analyze(node.arguments[0]).upper()

        if node.identifier == 'PRAY':
            if arg_type not in ['MARIA', 'EILEEN', 'GEHRMAN', 'BLOOD']:
                raise SemanticError(f"La función 'PRAY' solo puede imprimir valores de tipo 'MARIA', 'EILEEN', 'GEHRMAN', o 'BLOOD', pero se encontró '{arg_type}'", node)
        elif node.identifier == 'EYES':
            if arg_type not in ['MARIA', 'EILEEN']:
                raise SemanticError(f"La función 'EYES' solo puede leer valores de tipo 'MARIA' o 'EILEEN', pero se encontró '{arg_type}'", node)
        return None

    
    @semantic_error_handler
    def analyze_function_call(self, node):
        if node.identifier in ['PRAY', 'EYES']:
            return self._analyze_builtin_function_call(node)

        func_type = self.env.get_function_type(node.identifier.name)
        param_types, return_type = func_type

        if len(node.arguments or []) != len(param_types):
            raise SemanticError(
                f"La función '{node.identifier.name}' espera {len(param_types)} argumentos, pero se encontraron {len(node.arguments or [])}",
                node
            )

        for i, (arg, expected_type) in enumerate(zip(node.arguments, param_types)):
            arg_type = self.analyze(arg).upper()
            expected_type = expected_type.upper()
            if arg_type != expected_type:
                raise SemanticError(f"Argumento {i+1} de la función '{node.identifier.name}' esperaba '{expected_type}', pero se encontró '{arg_type}'", node)

        return return_type.upper()



    def _analyze_user_defined_function_call(self, node):
        func_type = self.env.get_function_type(node.identifier.name)
        param_types, return_type = func_type

        if len(node.arguments or []) != len(param_types):
            raise SemanticError(
                f"La función '{node.identifier.name}' espera {len(param_types)} argumentos, pero se encontraron {len(node.arguments or [])}",
                node
            )

        for i, arg in enumerate(node.arguments or []):
            arg_type = self.analyze(arg).upper()  
            expected_type = param_types[i].upper()  
            if arg_type != expected_type:
                raise SemanticError(f"Argumento {i+1} de la función '{node.identifier.name}' esperaba '{expected_type}', pero se encontró '{arg_type}'", node)

        return return_type.upper()


    def normalize_type(self, type_str):
        return type_str.upper() 

    @semantic_error_handler
    def analyze_if_statement(self, node):
        condition_type = self.analyze(node.condition)
        if condition_type != 'BLOOD':
            raise SemanticError("La condición en un 'Insight' debe ser de tipo 'BLOOD'", node.condition)
        
        self.analyze(node.true_block)
        
        current_node = node
        while current_node.false_block:
            if isinstance(current_node.false_block, IfStatementNode):
                current_node = current_node.false_block
                condition_type = self.analyze(current_node.condition)
                if condition_type != 'BLOOD':
                    raise SemanticError("La condición en un 'Madness Insight' debe ser de tipo 'BLOOD'", current_node.condition)
                self.analyze(current_node.true_block)
            else:
                self.analyze(current_node.false_block)
                break

    @semantic_error_handler
    def analyze_loop(self, node):
        if node.init:
            self.analyze(node.init)

        if not node.condition:
            raise SemanticError("El bucle debe tener una condición de tipo 'BLOOD'", node)

        condition_type = self.analyze(node.condition)
        if condition_type != 'BLOOD':
            raise SemanticError("La condición del bucle debe ser de tipo 'BLOOD'", node.condition)

        self.analyze(node.block)

        if node.increment:
            self.analyze(node.increment)


    @semantic_error_handler
    def analyze_unary_op(self, node):
        operand_type = self.analyze(node.operand)
        
        if node.operator == 'VILEBLOOD':
            if operand_type != 'BLOOD':
                raise SemanticError(f"El operador 'VILEBLOOD' solo se puede aplicar a valores de tipo 'BLOOD', pero se encontró '{operand_type}'", node)
            return 'BLOOD'
        else:
            raise SemanticError(f"Operador unario no soportado: {node.operator}", node)

    def analyze_function_declaration(self, node):
        param_types = [param_type for _, param_type in node.parameters]
        return_type = node.return_type.upper() 
        self.env.declare_function(node.name.name, param_types, return_type)
        self.env.enter_scope() 

        for param_name, param_type in node.parameters:
            self.env.declare_variable(param_name.name, param_type)

        self.analyze(node.block)

        if return_type != 'ROM': 
            if not self.has_return(node.block):
                raise SemanticError(f"La función '{node.name.name}' debe tener una instrucción de retorno de tipo '{return_type}'", node)

        self.env.exit_scope()


    @semantic_error_handler
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

    @semantic_error_handler
    def analyze_return(self, node):
        return_type = self.analyze(node.expression).upper()
        if return_type != 'MARIA':
            raise SemanticError(
                f"Error de tipo en retorno: se esperaba 'MARIA', pero se encontró '{return_type}'",
                node
            )
        return return_type
