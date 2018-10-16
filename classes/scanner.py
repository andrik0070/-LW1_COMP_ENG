from pprint import pprint

from classes.exceptions.main import EndStateException
from classes.fsm import fsm
from io import StringIO


class Scanner:
    def __init__(self, program_text_filename=None, keywords=[], states=[], start_state='Start'):
        self.fsm = fsm(states)
        self.program_text_filename = program_text_filename
        self.program_text = None
        self.keywords = keywords
        self.lexem_table = []
        self.start_state = start_state

    def load_text_from_file(self, program_text_filename=''):

        if program_text_filename:
            self.program_text_filename = program_text_filename

        with open(self.program_text_filename, 'r') as file:
            self.program_text = file.read().replace('\n', '')

    def run(self):
        fsm = self.fsm
        fsm.start(self.start_state)

        current_lexem = StringIO()

        for x in self.program_text:
            try:
                current_state = fsm.event(x)

                if not current_state[1]:
                    current_lexem.write(x)
                else:
                    if current_state[0] == 'Identifier':
                        if current_state[0] in self.keywords:
                            lexem_row = (current_lexem.getvalue(), 'Keyword')
                        else:
                            lexem_row = (current_lexem.getvalue(), 'Identifier')
                        self.lexem_table.append(lexem_row)
                    elif current_state[0] in ['NotEqual, Assign']:
                        self.lexem_table.append((current_lexem.getvalue(), 'OnePositionSeparator'))
                    else:
                        self.lexem_table.append((current_lexem.getvalue(), current_state[0]))
            except

        pprint(self.lexem_table)








            except EndStateException as e:
                pass
