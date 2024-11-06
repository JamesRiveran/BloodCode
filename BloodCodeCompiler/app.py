from flask import Flask, request, jsonify
from lexer.lexer import Lexer, Token
from parser.parser import Parser
from interpreter.interpreter import Interpreter
from semantic_analyzer.TypeEnviroment import TypeEnvironment
from semantic_analyzer.SemanticAnalyzer import SemanticAnalyzer
from semantic_analyzer.SemanticAnalyzer import SemanticError
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200

@app.route('/compile', methods=['POST'])
def compile_code():
    try:
        data = request.get_json()
        code = data.get('code', '')
        action = data.get('action', 'compile') 

        env = TypeEnvironment()
        lexer = Lexer(code)
        tokens: list[Token] = lexer.tokenize()

        if action == 'tokens':
            token_list = [token.to_dict() for token in tokens]
            return jsonify({'tokens': token_list}), 200

        parser = Parser(tokens)
        ast = parser.parse()

        if action == 'ast':
            return jsonify({'ast': repr(ast)}), 200  
        analyzer = SemanticAnalyzer(env)
        analyzer.analyze(ast)

        return jsonify({'message': 'Compilación exitosa'}), 200

    except SemanticError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Error inesperado: {str(e)}"}), 500

@app.route('/execute', methods=['POST'])
def execute_code():
    try:
        data = request.get_json()
        code = data.get('code', '')
        user_input = data.get('userInput', None) 

        env = TypeEnvironment()
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        analyzer = SemanticAnalyzer(env)
        analyzer.analyze(ast)

        interpreter = Interpreter(env)

        if user_input:
            interpreter.context["input_var"] = user_input

        interpreter.execute(ast)

        if interpreter.prompt_var: 
            return jsonify({"prompt": interpreter.prompt_var}), 200

        return jsonify({"output": interpreter.output}), 200

    except SemanticError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Error inesperado: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

