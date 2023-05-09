import numpy as np
import re

def check_dependencies(self):
    # clean of nan
    clean_structure = np.empty((0,))
    for entry in self.structure:
        if isinstance(entry, str):
            clean_structure = np.append(clean_structure, entry)
    self.structure = clean_structure

    # make structure and text array of equal length
    self.texts = self.texts[:len(self.structure)]

    # check dependencies
    # solve antwort problem
    if 'ITEM(Multiple)' in self.structure and 'ANSWER OPTION' in self.structure:
        self.structure[np.where(self.structure == 'ANSWER OPTION')] = 'SEVERAL ANSWER OPTIONS'

    if 'ITEM(Single)' in self.structure and 'ANSWER OPTION' in self.structure:
        self.structure[np.where(self.structure == 'ANSWER OPTION')] = 'SEVERAL ANSWER OPTIONS'

    # solve single choice with antwort problem
    if "ITEM(Single)" in self.structure and 'SEVERAL ANSWER OPTIONS' in self.structure:
        self.maxNumber = '1'
        self.structure = np.core.defchararray.replace(self.structure, 'ITEM(Single)', 'ITEM(Multiple)')
    else:
        self.maxNumber = 'null'

    # optional
    if 'OPTIONAL' in self.structure:
        self.answer_required = 'false'
        self.texts = np.delete(self.texts, np.where(self.structure == 'OPTIONAL'))
        self.structure = np.delete(self.structure, np.where(self.structure == 'OPTIONAL'))

    else:
        self.answer_required = 'true'

    # scala
    if 'SCALA' in self.structure:
        # Test Scala Texts:
        # Define the regular expression pattern
        pattern = r"(\d+)\s*\((\w+\s*\w+)\)\s*-\s*(\d+)\s*\((\w+\s*\w+)\)"
        if 'SCALA' in self.structure and not re.match(pattern, self.texts[np.where(self.structure == 'SCALA')][0]):
            raise Exception ('Scala Text is not correct: ', self.texts[np.where(self.structure == 'SCALA')][0])

        # declare numbers and texts     
        # get digits
        digits = re.findall(r'\d', self.texts[np.where(self.structure == 'SCALA')][0])
        self.scala_min = digits[0]
        self.scala_max = digits[1]
        texts = re.findall(r'\((.*?)\)', self.texts[np.where(self.structure == 'SCALA')][0])
        self.scala_min_text = texts[0]
        self.scala_max_text = texts[1]

    else:
        self.scala_min = None
        self.scala_max = None
        self.scala_min_text = None
        self.scala_max_text = None


def map_structure_to_type(structure):
    # ITEM_LIST_SINGLE_CHOICE (R): Item
    if "ITEM(Single)" in structure and not 'SEVERAL ANSWER OPTIONS' in structure:
        question_type = 'ITEM_LIST_SINGLE_CHOICE'
    # ITEM_LIST_EXPANDABLE (T OR C as answeroption): Item 
    elif 'ITEM(Multiple)' in structure or 'SEVERAL ANSWER OPTIONS' in structure:
        question_type = 'ITEM_LIST_EXPANDABLE'
        # ITEM_LIST_EXPANDABLE as single version
    elif "ITEM(Single)" in structure and 'SEVERAL ANSWER OPTIONS' in structure:
        question_type = 'ITEM_LIST_EXPANDABLE'
        # OPTION_QUESTION: S P Button
    elif 'Button' in structure:
        question_type = 'OPTION_QUESTION'
        # SCALA_SLIDER,
    elif 'SCALA' in structure:
        question_type = 'SCALA_SLIDER'
        # OPEN_QUESTION: S P Textfield
    elif 'ANSWER OPTION' in structure and not ("ITEM(Single)" or "ITEM(Multiple)") in structure:
        question_type = 'OPEN_QUESTION'
    elif 'Neue Etappe' in structure:
        question_type = 'Neue Etappe'
    else:
        question_type = 'CONTENT'

    return question_type


def map_structure_to_answer_option(structure, type):
    answer_option = ''
    # R = Radio Button
    for value in structure:
        if type == 'ITEM_LIST_SINGLE_CHOICE' and value == 'ITEM(Single)':
            answer_option += 'R'
        # C = Checkbox, 
        if type == 'ITEM_LIST_EXPANDABLE' and value == 'ITEM(Multiple)':
            answer_option += 'C'
        # T = Text_Field_Expandable
        if type == 'ITEM_LIST_EXPANDABLE' and value == 'SEVERAL ANSWER OPTIONS':
            answer_option += 'T'
    if answer_option == '':
        answer_option = None
    return answer_option

class Question:
    def __init__(self, structure, texts):
        self.structure = structure.values #array
        self.texts = texts.values #array
        # check dependencies and set structure and text right
        check_dependencies(self)
        self.type = map_structure_to_type(self.structure) 
        self.answer_option = map_structure_to_answer_option(self.structure, self.type)
        self.next_logic_type = 'NEXT'
        self.next_logic_option = None
        self.next_question_reference = None