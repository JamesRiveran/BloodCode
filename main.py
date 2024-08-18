from BloodCodeCompiler.lexer import Lexer

code = '''
Awaken {
    Chalice health: Blood => 100;
    Whisper "Welcome to Yharnam";
    
    Nightmare (health > 0) {
        Whisper "You are alive and well.";
    } HuntersMark (weapons == 0) {
        Whisper "You have no weapons!";
    } EternalRest {
        Whisper "Danger is imminent!";
    };

    BloodMoon (health > 0) {
        health => health + 20;
    };
};
'''

lexer = Lexer(code)
tokens = lexer.tokenize()

for token in tokens:
    print(token)
