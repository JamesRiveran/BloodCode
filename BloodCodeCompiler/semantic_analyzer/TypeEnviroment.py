class TypeEnvironment:
    def __init__(self):
        self.scopes = [{}]  # Lista de diccionarios, donde cada diccionario es un scope para variables
        self.functions = {}  # Diccionario global para almacenar las funciones y sus tipos

    def enter_scope(self):
        self.scopes.append({})  # Añadir un nuevo diccionario para el scope actual

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()  # Eliminar el scope actual
        else:
            raise Exception("No se puede salir del scope global")

    def declare_variable(self, name, var_type):
        if name in self.scopes[-1]:  # Verificar en el scope actual
            raise Exception(f"Variable '{name}' ya ha sido declarada en el scope actual")
        self.scopes[-1][name] = var_type  # Declarar en el scope actual

    def get_variable_type(self, name):
        for scope in reversed(self.scopes):  # Buscar desde el scope más interno hasta el global
            if name in scope:
                return scope[name]
        raise Exception(f"Variable '{name}' no ha sido declarada")

    def declare_function(self, name, param_types, return_type):
        if name in self.functions:
            raise Exception(f"Función '{name}' ya ha sido declarada")
        self.functions[name] = (param_types, return_type)

    def get_function_type(self, name):
        if name not in self.functions:
            raise Exception(f"Función '{name}' no ha sido declarada")
        return self.functions[name]
