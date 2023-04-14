'''class Question:
    def __init__(self, type, content='P', answer_option = None, next_logic_type='NEXT', next_logic_option=None):
        self.type = type
        self.content = content
        self.answer_option = answer_option
        self.next_logic_type = next_logic_type
        self.next_logic_option = next_logic_option
'''

def map_structure_to_type(structure):
    # ITEM_LIST_SINGLE_CHOICE (R): Item
    if "ITEM(Single)" in structure.values:
        question_type = 'ITEM_LIST_SINGLE_CHOICE'
    # ITEM_LIST_EXPANDABLE (T OR C as answeroption): Item 
    elif 'ITEM(Multiple)' in structure.values or 'Mehrere Antwortmöglichkeiten' in structure.values:
        question_type = 'ITEM_LIST_EXPANDABLE'
        # OPTION_QUESTION: S P Button
    elif 'Button' in structure.values:
        question_type = 'OPTION_QUESTION'
        # SCALA_SLIDER,
    elif 'SCALA' in structure.values:
        question_type = 'SCALA_SLIDER'
        # OPEN_QUESTION: S P Textfield
    elif 'Antwortmöglichkeit' in structure.values and not ("ITEM(Single)" or "ITEM(Multiple)") in structure.values:
        question_type = 'OPEN_QUESTION'
    else:
        question_type = 'CONTENT'

    return question_type

def map_structure_to_content(structure):
    content = ''
    for value in structure.values:
        if value == 'REFERENCE' or value == 'REFERENCE(Schlüsselerk.)':
            content += 'R'
        if value == 'IMAGE':
            content += 'I'
        if value == 'AUDIO':
            content += 'A'
        if value == 'PARAGRAPH':
            content += 'P'
        if value == 'MORE_INFORMATION':
            content += 'M'
    return content

def map_structure_to_answer_option(structure, type):
    answer_option = ''
    # R = Radio Button
    for value in structure.values:
        if type == 'ITEM_LIST_SINGLE_CHOICE' and value == 'ITEM(Single)':
            answer_option += 'R'
        # C = Checkbox, 
        if type == 'ITEM_LIST_EXPANDABLE' and value == 'ITEM(Multiple)':
            answer_option += 'C'
        # T = Text_Field_Expandable
        if type == 'ITEM_LIST_EXPANDABLE' and value == 'Mehrere Antwortmöglichkeiten':
            answer_option += 'T'
    if answer_option == '':
        answer_option = None
    return answer_option

def map_structure_to_next_logic_type(structure):
    #next_logic_type: NEXT, NEXT_OPTION, REF_KEY_INSIGHT
    if "REFERENCE(Schlüsselerk.)" in structure.values:
        next_logic_type = 'REF_KEY_INSIGHT'
    else: 
        next_logic_type = 'NEXT'
    return next_logic_type

class Question:
    def __init__(self, structure, texts):
        self.structure = structure #array
        self.texts = texts #array
        self.type = map_structure_to_type(self.structure) 
        self.content = map_structure_to_content(self.structure)
        self.answer_option = map_structure_to_answer_option(self.structure, self.type)
        self.next_logic_type= map_structure_to_next_logic_type(self.structure)
        self.next_logic_option = None