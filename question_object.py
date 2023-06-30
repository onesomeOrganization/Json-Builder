import numpy as np
import re
from refLogic_object import RefLogic
from content_object import Content
from answerOption_object import AnswerOption
from nextLogic_object import NextLogic
from helper import create_id


class Question:
    def __init__(self, trip, id_base, version, structure, texts, next_question_structure, next_question_texts, excel_id, write_beginning, write_ending):
        # VARIABLES
        self.reference_of_next_question = None
        self.next_logic_type = 'NEXT'
        self.id_base = id_base
        self.excel_id = excel_id
        self.next_question_structure = next_question_structure
        self.next_question_texts = next_question_texts
        self.write_beginning = write_beginning
        self.write_ending = write_ending
        self.etappe, self.screen = self.create_etappe_screen_from_id()
        self.version = version
        self.structure = structure.values #array
        self.texts = texts.values #array
        self.id = create_id(self, self.excel_id)
        self.trip = trip
        self.maxNumber = 'null'
        self.minNumber = 'null'
        self.firstJourneyQuestion = "null" 
        self.firstSessionQuestion = "null"

        # PREPARATIONS
        self.clear_of_nan()
        self.maxNumber = self.prep_type_and_clean_structure() # must be before map structure to type
        self.type = self.map_structure_to_type() 
        self.reviewable, self.worldObjectEntryKeyType, self.optional = self.prepare_keyInsight()
        # Variables for Building Blocks
        self.answer_required = self.prepare_optional()
        self.scala_min, self.scala_max, self.scala_min_text, self.scala_max_text = self.prepare_scala()
        self.adjust_min_max_number()
        
        # BUILDING BLOCKS
        self.RefLogic = RefLogic(self)
        self.NextLogic = NextLogic(self)
        self.clear_of_arrows()
        self.Content = Content(self)
        self.AnswerOption = AnswerOption(self)

        # JSON PREP
        self.comma_is_needed = self.check_if_comma_needed()

    # --------- PREPARATIONS -----------

    def clear_of_arrows(self):
        # arrow logics
        for num, struc in enumerate(self.structure):
            if struc == 'ITEM(Single)' and '->' in self.texts[num]:
                self.texts[num] = self.texts[num].split('->')[0].strip()

    def create_etappe_screen_from_id(self):
        etappe = self.excel_id.split('.')[0]
        screen = self.excel_id.split('.')[1]
        return etappe, screen
    
    def map_structure_to_type(self):
        # ITEM_LIST_SINGLE_CHOICE (R): Item
        if "ITEM(Single)" in self.structure and not 'SEVERAL ANSWER OPTIONS' in self.structure:
            question_type = 'ITEM_LIST_SINGLE_CHOICE'
        # ITEM_LIST_EXPANDABLE (T OR C as answeroption): Item 
        elif 'ITEM(Multiple)' in self.structure or 'SEVERAL ANSWER OPTIONS' in self.structure:
            question_type = 'ITEM_LIST_EXPANDABLE'
            # ITEM_LIST_EXPANDABLE as single version
        elif "ITEM(Single)" in self.structure and 'SEVERAL ANSWER OPTIONS' in self.structure:
            question_type = 'ITEM_LIST_EXPANDABLE'
            # ITEM_LIST_EXPANDABLE without items but with textfield expandable
        elif 'SEVERAL ANSWER OPTIONS' in self.structure:
            question_type = 'ITEM_LIST_EXPANDABLE'
            # OPTION_QUESTION: S P Button
        elif 'BUTTON' in self.structure:
            question_type = 'OPTION_QUESTION'
            # SCALA_SLIDER,
        elif 'SCALA' in self.structure:
            question_type = 'SCALA_SLIDER'
            # OPEN_QUESTION: S P Textfield
        elif 'ANSWER OPTION' in self.structure and not ("ITEM(Single)" or "ITEM(Multiple)") in self.structure:
            question_type = 'OPEN_QUESTION'
        elif 'Neue Etappe' in self.structure:
            question_type = 'Neue Etappe'
        else:
            question_type = 'CONTENT'

        return question_type
    
    def clear_of_nan(self):
        # CLEAN OF NAN
        clean_structure = np.empty((0,))
        for entry in self.structure:
            if isinstance(entry, str):
                clean_structure = np.append(clean_structure, entry)
        self.structure = clean_structure

        # make structure and text array of equal length
        self.texts = self.texts[:len(self.structure)]

    def prep_type_and_clean_structure(self):
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
            
        return self.maxNumber
    
    def adjust_min_max_number(self):
        if self.type == 'SCALA_SLIDER':
            self.minNumber = self.scala_min
            self.maxNumber = self.scala_max

        if self.type == 'ITEM_LIST_EXPANDABLE':
            self.minNumber = 1
        
    def prepare_optional(self):
        # OPTIONAL
        if 'OPTIONAL' in self.structure:
            self.answer_required = 'false'
            self.texts = np.delete(self.texts, np.where(self.structure == 'OPTIONAL'))
            self.structure = np.delete(self.structure, np.where(self.structure == 'OPTIONAL'))

        else:
            self.answer_required = 'true'
        return self.answer_required

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
        return self.scala_min, self.scala_max, self.scala_min_text, self.scala_max_text
    
    def prepare_keyInsight(self):
        # take care of optional/verpflichtende Schlüsselerkenntnisse
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

        return self.reviewable, self.worldObjectEntryKeyType, self.optional

    
    # ------------ JSON ---------------
    
    def check_if_comma_needed(self):
        if any(element == 'Neue Etappe' for element in self.next_question_structure):
            comma_is_needed = False
        elif all(element == 'None' for element in self.next_question_structure):
            comma_is_needed = False
        else:
            comma_is_needed = True
        return comma_is_needed

    def create_json(self):
        # last prep (geht erst hier weil es etappenstartscreens davor nicht gibt)
        if (self.screen == 0 and self.write_beginning == True) or self.excel_id in self.trip.etappen_start_screens:
            self.firstJourneyQuestion = "true" 
            self.firstSessionQuestion = "true"
        
        if self.type == 'Neue Etappe':
            return self.create_neue_etappe()

        json = '''
            {
            "id": "%s",
            "type": "%s",
            "number": null,
            "minNumber": %s,
            "maxNumber": %s,
            "screenDuration": null,
            "reviewAble": %s,
            "noAnswerPreselection": null,
            "showHint": null,
            "progress": %s,
            "worldObjectEntryKeyType": %s,
            "nonOptionalKeyInsightHint": false,
            "optional": %s,
            "firstJourneyQuestion": %s,
            "firstSessionQuestion": %s,
            "questionLoopId": null,
            "translations": [],
            "content": [
                %s
                %s
            ],
            %s
            },''' %(self.id, self.type, self.minNumber, self.maxNumber, self.reviewable, self.progress, self.worldObjectEntryKeyType, self.optional, self.firstJourneyQuestion, self.firstSessionQuestion, self.Content.json, self.AnswerOption.json, self.NextLogic.json)
        
        if self.comma_is_needed:
            return json
        else:
            return json[:-1]

    
    def create_neue_etappe(self):
        # Preparations
        order = self.etappe
        id = self.id_base + 'v' + self.version + '-'+ self.etappe
        durationMin =  int(self.texts[np.where(self.structure == 'Zeit min')][0]) if 'Zeit min' in self.structure else ''
        durationMax = int(self.texts[np.where(self.structure == 'Zeit max')][0]) if 'Zeit max' in self.structure else ''
        title = self.texts[np.where(self.structure == 'Etappen-Titel')][0] if 'Etappen-Titel' in self.structure else ''

        # Json
        json = '''
            ],
        "questionLoops": []
        },
        {
        "id": "%s",
        "order": %s,
        "durationMin": %s,
        "durationMax": %s,
        "translations": [
            {
            "id": "%s-DE",
            "language": "DE",
            "title": "%s"
            },
            {
            "id": "%s-EN",
            "language": "EN",
            "title": "Englisch"
            }
        ],
        "questions": [
            '''%(id, order, durationMin, durationMax, id, title, id)
        
        return json