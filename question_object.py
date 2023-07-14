import numpy as np
import re
from refLogic_object import RefLogic
from content_object import Content
from answerOption_object import AnswerOption
from nextLogic_object import NextLogic
from helper import create_id
from tests import do_tests_on_questions


class Question:
    def __init__(self, trip, id_base, version, structure, texts, texts_en, next_question_structure, next_question_texts, excel_id, write_beginning, write_ending, english_translation):
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
        self.texts_en = texts_en.values
        self.english_translation = english_translation
        self.id = create_id(self, self.excel_id)
        self.trip = trip
        self.maxNumber = 'null'
        self.minNumber = 'null'
        self.firstJourneyQuestion = "null" 
        self.firstSessionQuestion = "null"

        # TEST
        do_tests_on_questions(self)

        # PREPARATIONS    
        self.clear_of_nan()
        self.answer_required = self.prepare_optional()
        self.type, self.maxNumber = self.map_structure_to_type() 
        self.reviewable, self.worldObjectEntryKeyType, self.optional = self.prepare_keyInsight()
        self.prepare_multiple_references()
        # Variables for Building Blocks
        self.scala_min, self.scala_max, self.scala_min_text, self.scala_max_text, self.scala_max_text_en, self.scala_min_text_en = self.prepare_scala()
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

    def prepare_multiple_references(self):
        for i, struc in enumerate(self.structure):
            # find references with "und"
            if struc == 'REFERENCE' and 'und' in self.texts[i]:
                splits = self.texts[i].split('und')
                self.texts[i] = splits[0].strip()
                if self.english_translation:
                    self.texts_en[i] = splits[0].strip()
                # insert another reference
                for num in range(1, len(splits)):
                    self.structure = np.insert(self.structure,i+1,'REFERENCE')
                     # split text to the references
                    self.texts = np.insert(self.texts,i+num,splits[num].strip())
                    if self.english_translation:
                        self.texts_en = np.insert(self.texts_en,i+num,splits[num].strip())


    def clear_of_arrows(self):
        # arrow logics
        for num, struc in enumerate(self.structure):
            if (struc == 'ITEM(Single)' and '->' in self.texts[num]) or (struc == 'ITEM(Multiple)' and self.maxNumber == '1' and '->' in self.texts[num]):
                self.texts[num] = self.texts[num].split('->')[0].strip()
                if self.english_translation:
                    self.texts_en[num] = self.texts_en[num].split('->')[0].strip()

    def create_etappe_screen_from_id(self):
        etappe = self.excel_id.split('.')[0]
        screen = self.excel_id.split('.')[1]
        return etappe, screen
    
    def map_structure_to_type(self):
        # ITEM_LIST_SINGLE_CHOICE: nur wenn es single items sind und es keinerlei asnweroption gibt
        if "ITEM(Single)" in self.structure and not ('SEVERAL ANSWER OPTIONS' in self.structure or 'ANSWER OPTON' in self.structure):
            question_type = 'ITEM_LIST_SINGLE_CHOICE'
            # single choice and i= in answers 
            for text in self.texts:
                if 'i=' in text or 'i =' in text:
                    self.maxNumber = '1'
                    self.structure = np.core.defchararray.replace(self.structure, 'ITEM(Single)', 'ITEM(Multiple)')
                    question_type = 'ITEM_LIST_LIMIT'
        elif 'ITEM(Multiple)' in self.structure and not ('SEVERAL ANSWER OPTIONS' in self.structure or 'ANSWER OPTON' in self.structure):
            question_type = 'ITEM_LIST_LIMIT'
            if self.answer_required:
                self.minNumber = '1'
        # ITEM_LIST_EXPANDABLE: A) entweder mehrere text felder ohne items oder B) item multiple mit text feldern oder C) item single mit text feldern und maxnumber
            # A
        elif not ('ITEM(Multiple)' in self.structure or "ITEM(Single)" in self.structure) and 'SEVERAL ANSWER OPTIONS' in self.structure:
            question_type = 'ITEM_LIST_EXPANDABLE'
            # B
        elif 'ITEM(Multiple)' in self.structure and ('SEVERAL ANSWER OPTIONS' in self.structure or 'ANSWER OPTON' in self.structure):
            question_type = 'ITEM_LIST_EXPANDABLE'
            # C
        elif "ITEM(Single)" in self.structure and ('SEVERAL ANSWER OPTIONS' in self.structure or 'ANSWER OPTON' in self.structure):
            self.maxNumber = '1'
            self.structure = np.core.defchararray.replace(self.structure, 'ITEM(Single)', 'ITEM(Multiple)')
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

        return question_type, self.maxNumber
    
    def clear_of_nan(self):
        # CLEAN OF NAN
        clean_structure = np.empty((0,))
        for entry in self.structure:
            if isinstance(entry, str) and entry != 'None':
                clean_structure = np.append(clean_structure, entry)
        self.structure = clean_structure

        # make structure and text array of equal length
        self.texts = self.texts[:len(self.structure)]
        if self.english_translation:
            self.texts_en = self.texts_en[:len(self.structure)]
    
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
            self.texts_en = np.delete(self.texts_en, np.where(self.structure == 'OPTIONAL'))
            self.structure = np.delete(self.structure, np.where(self.structure == 'OPTIONAL'))

        else:
            self.answer_required = 'true'
        return self.answer_required

    def prepare_scala(self):
        # SCALA
        if 'SCALA' in self.structure:
            # declare numbers and texts     
            # get digits
            digits = re.findall(r'\d', self.texts[np.where(self.structure == 'SCALA')][0])
            self.scala_min = digits[0]
            self.scala_max = digits[1]
            texts = re.findall(r'\((.*?)\)', self.texts[np.where(self.structure == 'SCALA')][0])
            self.scala_min_text = texts[0]
            self.scala_max_text = texts[1]

            if self.english_translation:
                texts_en = re.findall(r'\((.*?)\)', self.texts_en[np.where(self.structure == 'SCALA')][0])
                self.scala_min_text_en = texts_en[0]
                self.scala_max_text_en = texts_en[1]
            else:
                self.scala_max_text_en = 'Englisch'
                self.scala_min_text_en = 'Englisch'
        else:
            self.scala_min = None
            self.scala_max = None
            self.scala_min_text = None
            self.scala_max_text = None
            self.scala_max_text_en = None
            self.scala_min_text_en = None
        return self.scala_min, self.scala_max, self.scala_min_text, self.scala_max_text, self.scala_max_text_en, self.scala_min_text_en
    
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

        if self.english_translation:
            title_en = self.texts_en[np.where(self.structure == 'Etappen-Titel')][0] if 'Etappen-Titel' in self.structure else ''
        else:
            title_en = 'Englisch'

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
            "title": "%s"
            }
        ],
        "questions": [
            '''%(id, order, durationMin, durationMax, id, title, id, title_en)
        
        return json