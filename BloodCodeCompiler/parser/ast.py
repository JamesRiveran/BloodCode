class ASTNode:
    def __init__(self, line_number):
        self.line_number = line_number 


class IdentifierNode(ASTNode):
    def __init__(self, name, line_number):
        super().__init__(line_number)
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"


class NumberNode(ASTNode):
    def __init__(self, value, line_number):
        super().__init__(line_number)
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"


class StringNode(ASTNode):
    def __init__(self, value, line_number):
        super().__init__(line_number)
        self.value = value

    def __repr__(self):
        return f"String({self.value})"


class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right, line_number):
        super().__init__(line_number)
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.left}, {self.operator}, {self.right})"


class DeclarationNode(ASTNode):
    def __init__(self, identifier_list, var_type, expression=None, line_number=None):
        super().__init__(line_number)
        self.identifier_list = identifier_list
        self.var_type = var_type
        self.expression = expression

    def __repr__(self):
        return f"Declaration({self.identifier_list}, {self.var_type}, {self.expression})"


class BlockNode(ASTNode):
    def __init__(self, statements, line_number=None):
        super().__init__(line_number)
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"


class IfStatementNode(ASTNode):
    def __init__(self, condition, true_block, false_block=None, line_number=None):
        super().__init__(line_number)
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def __repr__(self):
        return f"If({self.condition}, {self.true_block}, {self.false_block})"


class LoopNode(ASTNode):
    def __init__(self, init, condition, increment, block, line_number=None):
        super().__init__(line_number)
        self.init = init
        self.condition = condition
        self.increment = increment
        self.block = block

    def __repr__(self):
        return f"Loop({self.init}, {self.condition}, {self.increment}, {self.block})"


class FunctionCallNode(ASTNode):
    def __init__(self, identifier, arguments, line_number=None):
        super().__init__(line_number)
        self.identifier = identifier
        self.arguments = arguments

    def __repr__(self):
        return f"FunctionCall({self.identifier}, {self.arguments})"


class RestNode(ASTNode):
    def __init__(self, line_number=None):
        super().__init__(line_number)

    def __repr__(self):
        return "Rest()"


class BooleanNode(ASTNode):
    def __init__(self, value, line_number=None):
        super().__init__(line_number)
        self.value = value

    def __repr__(self):
        return f"Boolean({self.value})"


class UnaryOpNode(ASTNode):
    def __init__(self, operator, operand, line_number=None):
        super().__init__(line_number)
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"UnaryOp({self.operator}, {self.operand})"


class FunctionDeclarationNode(ASTNode):
    def __init__(self, name, parameters, return_type, block, line_number=None):
        super().__init__(line_number)
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.block = block


class ReturnNode(ASTNode):
    def __init__(self, expression, line_number=None):
        super().__init__(line_number)
        self.expression = expression


class ArrayNode(ASTNode):
    def __init__(self, elements, line_number=None):
        super().__init__(line_number)
        self.elements = elements

    def __repr__(self):
        return f"Array({self.elements})"
