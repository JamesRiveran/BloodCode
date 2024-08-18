import unittest
from BloodCodeCompiler.lexer import Lexer

class TestLexer(unittest.TestCase):
    def test_basic_tokens(self):
        code = '''
        Awaken {
            Chalice health: Blood => 100;
            Whisper "Welcome to Yharnam";
        };
        '''
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected_tokens = [
            ('AWAKEN', 'Awaken'),
            ('LBRACE', '{'),
            ('CHALICE', 'Chalice'),
            ('IDENTIFIER', 'health'),
            ('COLON', ':'),
            ('IDENTIFIER', 'Blood'),
            ('ASSIGN', '=>'),
            ('NUMBER', '100'),
            ('SEMICOLON', ';'),
            ('WHISPER', 'Whisper'),
            ('STRING', '"Welcome to Yharnam"'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}'),
            ('SEMICOLON', ';')
        ]
        self.assertEqual(tokens, expected_tokens)

if __name__ == '__main__':
    unittest.main()
