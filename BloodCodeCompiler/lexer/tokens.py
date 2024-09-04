import re

tokens = [
    ('NIGHTMARE', r'Nightmare'),
    ('DREAM', r'Dream'),
    ('HUNTER', r'Hunter'),
    ('HUNTERS', r'Hunters')
    ('GREATONES', r'GreatOnes'),
    ('DJURA', r'Djura'),
    ('EILEEN', r'Eileen'),
    ('BLOOD', r'Blood'),
    ('MARIA', r'Maria'),
    ('GEHRMAN', r'Gehrman'),
    ('ROM', r'Rom'),
    ('DRUNKENNESS', r'Drunkenness'),
    ('REST', r'Rest'),
    ('INSIGHT', r'Insight'),
    ('MADNESS', r'Madness'),
    ('EYES', r'Eyes'),
    ('PRAY', r'Pray'),
    ('VILEBLOOD', r'Vileblood'),
    ('BLOODBOND', r'Bloodbond'),
    ('OLDBLOOD', r'OldBlood'),

    ('GREATER', r'>'),
    ('LESS', r'<'),
    ('GREATEREQUAL', r'>='),
    ('LESSEQUAL', r'<='),
    ('EQUAL', r'=='),
    ('ASSIGN', r'=>'),
    ('NOT', r'!='),
    ('COLON', r':'),
    ('LEFTPARENTHESIS', r'\('),
    ('RIGHTPARENTHESIS', r'\)'),
    ('LEFTBRACE', r'\{'),
    ('RIGHTBRACE', r'\}'),
    ('COMMA', r','),
    ('SEMICOLON', r';'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULTIPLY', r'\*'),
    ('DIVIDE', r'/'),

    ('LIGHT', r'Light'),
    ('DARKNESS', r'Darkness'),
    ('COMMENT', r'//.*'),
    ('WHITESPACE', r'\s+'),

    ('NUMBER', r'\d+(\.\d+)?'),
    ('STRING', r'"[^"]*"'),
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),
]

# Compile tokens with re.IGNORECASE to ignore case sensitivity
compiled_tokens = [(name, re.compile(pattern, re.IGNORECASE)) for name, pattern in tokens]
