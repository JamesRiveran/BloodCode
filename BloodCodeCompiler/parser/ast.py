class ASTNode:
    pass

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"String({self.value})"

class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.left}, {self.operator}, {self.right})"

class DeclarationNode(ASTNode):
    def __init__(self, identifier_list, var_type, expression=None):
        self.identifier_list = identifier_list
        self.var_type = var_type
        self.expression = expression

    def __repr__(self):
        return f"Declaration({self.identifier_list}, {self.var_type}, {self.expression})"

class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"

class IfStatementNode(ASTNode):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def __repr__(self):
        return f"If({self.condition}, {self.true_block}, {self.false_block})"

class LoopNode(ASTNode):
    def __init__(self, init, condition, increment, block):
        self.init = init
        self.condition = condition
        self.increment = increment
        self.block = block

    def __repr__(self):
        return f"Loop({self.init}, {self.condition}, {self.increment}, {self.block})"

class FunctionCallNode(ASTNode):
    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments = arguments

    def __repr__(self):
        return f"FunctionCall({self.identifier}, {self.arguments})"

class RestNode(ASTNode):
    def __init__(self):
        pass

    def __repr__(self):
        return "Rest()"
      
class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Boolean({self.value})"
        
class UnaryOpNode(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"UnaryOp({self.operator}, {self.operand})"
      
class FunctionDeclarationNode(ASTNode):
    def __init__(self, name, parameters, return_type, block):
        self.name = name   
        self.parameters = parameters  
        self.return_type = return_type 
        self.block = block  

class ReturnNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression 

class ArrayNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements 
