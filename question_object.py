import numpy as np
import re


def create_id (self, reference_id_excel):
    reference_id_excel = reference_id_excel.strip()
    id_numbers = reference_id_excel.split('.')
    new_id = self.id_base + self.version + '-'+ id_numbers[0]+'-'+ id_numbers[1]
    return new_id

def create_etappe_screen_from_id(self):
    etappe = self.id.split('.')[0]
    screen = self.id.split('.')[1]
    return etappe, screen

def clear_of_nan(self):
    # CLEAN OF NAN
    clean_structure = np.empty((0,))
    for entry in self.structure:
        if isinstance(entry, str):
            clean_structure = np.append(clean_structure, entry)
    self.structure = clean_structure

    # make structure and text array of equal length
    self.texts = self.texts[:len(self.structure)]

def solve_answer_problem(self):
    # SOLVE ANTWORT PROBLEM -> with item it is always a several answer options field
    if 'ITEM(Multiple)' in self.structure and 'ANSWER OPTION' in self.structure:
        self.structure[np.where(self.structure == 'ANSWER OPTION')] = 'SEVERAL ANSWER OPTIONS'
    if 'ITEM(Single)' in self.structure and 'ANSWER OPTION' in self.structure:
        self.structure[np.where(self.structure == 'ANSWER OPTION')] = 'SEVERAL ANSWER OPTIONS'

    # SINGLE CHOICE WITH ANTWORT
    if "ITEM(Single)" in self.structure and 'SEVERAL ANSWER OPTIONS' in self.structure:
        self.maxNumber = '1'
        self.structure = np.core.defchararray.replace(self.structure, 'ITEM(Single)', 'ITEM(Multiple)')
    else:
        self.maxNumber = 'null'

def prepare_optional(self):
    # OPTIONAL
    if 'OPTIONAL' in self.structure:
        self.answer_required = 'false'
        self.texts = np.delete(self.texts, np.where(self.structure == 'OPTIONAL'))
        self.structure = np.delete(self.structure, np.where(self.structure == 'OPTIONAL'))

    else:
        self.answer_required = 'true'

def prepare_scala(self):
    # SCALA
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

def prepare_button(self):
    # BUTTONS
    if 'BUTTON' in self.structure:
        self.next_logic_type = 'NEXT_OPTION'
        self.next_logic_option = 'NN'
        # Test -> for buttons
        button_texts = self.texts[np.where(self.structure == 'BUTTON')]
        for button_text in button_texts:
            if not '->' in button_text:
                raise Exception ('"->" missing at one of the Buttons')
        button_one = button_texts[0].split('->')
        button_two = button_texts[1].split('->')
        self.button_one_text = button_one[0].strip()
        self.button_two_text = button_two[0].strip()
        self.next_logic_option_screen_refs.append(create_id(self, button_one[1]))
        self.next_logic_option_screen_refs.append(create_id(self, button_two[1]))
    else:
        self.button_one_text = None
        self.button_two_text = None

def prepare_keyInsight(self):
     # KEY INSIGHT
    if 'KEY INSIGHT (optional)' in self.structure or 'KEY INSIGHT (verpflichtend)' in self.structure:
        self.reviewable = 'true'
        if 'KEY INSIGHT (optional)' in self.structure:
            self.worldObjectEntryKeyType = '"'+ self.texts[np.where(self.structure == 'KEY INSIGHT (optional)')][0]+'"'
            self.optional = 'true'
        elif 'KEY INSIGHT (verpflichtend)' in self.structure:
            self.worldObjectEntryKeyType = '"'+self.texts[np.where(self.structure == 'KEY INSIGHT (verpflichtend)')][0]+'"'
            self.optional = 'false'
    else:
        self.reviewable = 'false'
        self.worldObjectEntryKeyType = 'null'
        self.optional = 'true'

def prepare_nextLogic(self):
    # NEXT OPTIONS ITEMS
    for num, struc in enumerate(self.structure):
        if struc == 'ITEM(Single)' and '->' in self.texts[num]:
            self.next_logic_option += 'N'
            self.next_logic_type = 'NEXT_OPTION'
            self.next_logic_option_screen_refs.append(create_id(self, self.texts[num].split('->')[1]))
            self.texts[num] = self.texts[num].split('->')[0].strip()


def prepare_refLogic(self):
    self.refLogic_type = None
    self.refLogic_options = {}
    # check for "sonst" in Reference
    if 'REFERENCE' in self.structure:
        ref_text = self.texts[np.where(self.structure == 'REFERENCE')][0]
        if 'sonst' in ref_text:
            # if found set self.refLogic_type to REF_OPTIONAL
            self.refLogic_type = 'REF_OPTIONAL'
            # Add key without a value
            self.refLogic_options['OPTION'] = []
            # count how many and create options as self.refLogics
            splits = ref_text.split('sonst')
            for split in splits:
                self.refLogic_options['OPTION'].append(create_id(self, split))
            # set text to '' else it will appear in worldobjectentry
            self.texts[np.where(self.structure == 'REFERENCE')] = 'null'


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
        # ITEM_LIST_EXPANDABLE without items but with textfield expandable
    elif 'SEVERAL ANSWER OPTIONS' in structure:
        question_type = 'ITEM_LIST_EXPANDABLE'
        # OPTION_QUESTION: S P Button
    elif 'BUTTON' in structure:
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
        if type == 'ITEM_LIST_EXPANDABLE' and value == 'SEVERAL ANSWER OPTIONS' and not ('ITEM(Multiple)' or 'ITEM(Single)') in structure:
            answer_option += 'T'
    if answer_option == '':
        answer_option = None
    return answer_option

class Question:
    def __init__(self, id_base, version, structure, texts, id):
        self.id_base = id_base
        self.id = id
        self.etappe, self.screen = create_etappe_screen_from_id(self)
        self.version = version
        self.structure = structure.values #array
        self.texts = texts.values #array
        self.next_logic_type = 'NEXT'
        self.next_logic_option = ''
        self.next_logic_option_screen_refs = []
        # PREPARATIONS
        clear_of_nan(self)
        solve_answer_problem(self)
        prepare_optional(self)
        prepare_scala(self)
        prepare_button(self)
        prepare_keyInsight(self)
        prepare_nextLogic(self)
        prepare_refLogic(self)
        self.type = map_structure_to_type(self.structure) 
        self.answer_option = map_structure_to_answer_option(self.structure, self.type)
        self.reference_of_next_question = None

        