from classes.fsm import fsm
from classes.scanner import Scanner

keywords = [
      'procedure', 'var', 'Integer', 'TDrawBuffer', 'Begin', 'if', 'and', 'then', 'End'
]

transitions = [
    ("Start", "Start", lambda x: x == ' ', False),
    ("Start", "Integer", lambda x: x.isdigit(), False),
    ("Integer", "Integer", lambda x: x.isdigit(), False),
    ("Integer", "Integer", lambda x: x == ' ', True),

    ("Start", "Identifier", lambda x: x.isalpha(), False),

    ("Identifier", "Identifier", lambda x: x.isalnum(), False),
    ("Identifier", "Identifier", lambda x: x == ' ', True),

    ("Start", "Colon", lambda x: x == ':', False),
    ("Colon", "Assign", lambda x: x == '=', False),
    ("Colon", "Delimiter", lambda x: x == ' ', True),
    ("Assign", "Assign", lambda x: x == ' ', True),

    ("Start", "Less", lambda x: x == '<', False),
    ("Less", "NotEqual", lambda x: x == '>', False),
    ("Less", "Delimiter", lambda x: x == ' ', True),
    ("NotEqual", "NotEqual", lambda x: x == ' ', True),

    ("Start", "Delimiter", lambda x: x in ['.', ';', '(', ')', '=', '-', ',', '[', ']'], False),
    ("Delimiter", "Delimiter", lambda x: x == ' ', True),

    ("Start", "StringLiteral", lambda x: x == "'", False),
    ("StringLiteral", "StringLiteral", lambda x: x != "'", False),
    ("StringLiteral", "StringLiteral", lambda x: x == "'", True),
    # ("StringLiteral", "StringLiteralEnd", lambda x: x == "'", False),
    # ("StringLiteralEnd", "StringLiteralEnd", lambda x: x == ' ', True),


]

scanner = Scanner('./data/program_text.txt', keywords, transitions)
scanner.load_text_from_file()
scanner.run()


# fs = fsm(transitions)
# fs.start("Start")
