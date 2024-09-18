import re
from BloodCodeCompiler.lexer.lexer import Lexer
from BloodCodeCompiler.parser.parser import Parser
from BloodCodeCompiler.interpreter.interpreter import Interpreter
from BloodCodeCompiler.semantic_analyzer.SemanticAnalyzer import SemanticAnalyzer, SemanticError
from BloodCodeCompiler.semantic_analyzer.TypeEnviroment import TypeEnvironment


def main():
    code = '''
HuntersDream {
    Hunter a, b, c: Maria;
    Hunter result: Maria;
    Hunter isTrue: Blood => true;
    Hunter greeting: Eileen => "Hello, Bloodborne!";
    Hunter numbers: Maria[5] => [1, 2, 3, 4, 5];

    a => 10;
    b => 5;
    c => 3;
    result => a + b * c - (a / b) + (a * b - c);  
    Pray(result);

    Insight (a > b) {
        Pray("a es mayor que b");
    } Madness {
        Pray("a no es mayor que b");
    }

    Dream (b > 0) {
        Pray(b);
        b => b - 1;
    }

    Nightmare (Hunter i: Maria => 0; i < 5; i => i + 1) {
        Pray("Índice:");
        Pray(i);
        Pray("Valor en numbers:");
        Pray(numbers[i]);
    }

    GreatOnes sum(Hunter x: Maria, Hunter y: Maria): Maria {
        Echoes(x + y);
    }

    Hunter total: Maria => sum(a, c);
    Pray("La suma de a y c es:");
    Pray(total);
}

}

    '''
    env = TypeEnvironment()
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    print("Código fuente:")
    print(code)
    
    try:
        ast = parser.parse()
        print("AST:", ast)
        analyzer = SemanticAnalyzer(env)
        analyzer.analyze(ast)
        interpreter = Interpreter(env)
        interpreter.execute(ast)
        print("Contexto:", interpreter.context)
    except SemanticError as e:
        print(e) 
    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()
