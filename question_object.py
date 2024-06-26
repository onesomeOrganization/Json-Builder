import numpy as np
import re
from refLogic_object import RefLogic
from content_object import Content
from answerOption_object import AnswerOption
from nextLogic_object import NextLogic
from helper import create_id
from tests import do_tests_on_questions, test_if_id_exists, test_for_correct_key_insight, test_for_text_without_structure
import pandas as pd


class Question:
    def __init__(self, trip, id_base, version, structure, texts, texts_en, next_question_structure, next_question_texts, excel_id, write_beginning, write_ending, english_translation, questions_before):
        # VARIABLES
        self.reference_of_next_question = None
        self.next_logic_type = 'NEXT'
        self.next_question_structure = next_question_structure
        self.next_question_texts = next_question_texts
        self.write_beginning = write_beginning
        self.write_ending = write_ending
        self.questions_before = questions_before
        self.id_base = id_base
        self.excel_id = excel_id
        test_if_id_exists(self)
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
        self.qloop_start = self.check_if_qloop_start()
        self.progress = None
        self.questionLoopId = 'null'
        self.reference_style = 'null'

        # TEST
        self.clear_of_nan()
        self.format_text()
        do_tests_on_questions(self)

        # PREPARATIONS    
        self.question_answer_option_ref()
        self.answer_required = self.prepare_optional()
        self.scala_min, self.scala_max, self.scala_min_text, self.scala_max_text, self.scala_max_text_en, self.scala_min_text_en = self.prepare_scala()
        self.type, self.maxNumber, self.minNumber = self.map_structure_to_type() 
        self.adjust_type_to_questionloop()
        self.reviewable, self.worldObjectEntryKeyType, self.optional = self.prepare_keyInsight()
        self.prepare_multiple_references()
        
        # BUILDING BLOCKS
        self.RefLogic = RefLogic(self)
        self.NextLogic = NextLogic(self)
        #self.clear_of_arrows()
        self.Content = Content(self)
        self.AnswerOption = AnswerOption(self)

        # JSON PREP
        self.comma_is_needed = self.check_if_comma_needed()

    # --------- PREPARATIONS -----------

    def question_answer_option_ref(self):
        for i,text in enumerate(self.texts):
            if '[Antwort Start Questionloop]' in text:
                self.texts[i] = text.replace('[Antwort Start Questionloop]', '{QUESTION_ANSWER_OPTION_REF}')

    def check_if_qloop_start(self):
        qloop_start = False
        for struc in self.structure:
            if struc == 'Start Questionloop':
                qloop_start = True
        return qloop_start


    def format_text(self):
        for i, text in enumerate(self.texts):
              if not pd.isnull(text):
              # find " and replace with \"
              # find breaks and delete them
                self.texts[i] = text.replace('\n', '').replace("_x000B_", "").replace('\u2028','').replace('"', '\\"').replace('\\\\"', '\\"')

        if self.english_translation:
            for i, text in enumerate(self.texts_en):
                if not pd.isnull(text):
                # find " and replace with \"
                # find breaks and delete them
                    self.texts_en[i] = text.replace('"', '\\"').replace('\n', '').replace("_x000B_", "").replace('\u2028','').replace('\\\\"', '\\"')

    def prepare_multiple_references(self):
        new_structure = np.array([])
        new_texts = np.array([])
        for i, struc in enumerate(self.structure):
            
            # find references with "und"
            if struc == 'REFERENCE' and 'und' in self.texts[i]:
                splits = self.texts[i].split('und')
                for split in splits:
                    new_structure = np.append(new_structure, 'REFERENCE')
                    new_texts = np.append(new_texts,split.strip())
            else:
                new_structure = np.append(new_structure, struc)
                new_texts = np.append(new_texts, self.texts[i])

        self.texts = new_texts
        self.structure = new_structure

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
        # ITEM_LIST_EXPANDABLE: A) entweder mehrere text felder ohne items oder B) item multiple mit text feldern
            # A
        elif not ('ITEM(Multiple)' in self.structure or "ITEM(Single)" in self.structure) and 'SEVERAL ANSWER OPTIONS' in self.structure and not 'ANSWER OPTIONS FROM REFERENCE (Multiple Choice)' in self.structure:
            question_type = 'ITEM_LIST_EXPANDABLE'
            # B
        elif 'ITEM(Multiple)' in self.structure and ('SEVERAL ANSWER OPTIONS' in self.structure or 'ANSWER OPTON' in self.structure):
            question_type = 'ITEM_LIST_EXPANDABLE'
        # ITEM_LIST_EXPANDABLE_SINGLE_CHOICE: item single mit text feldern und maxnumber
        elif "ITEM(Single)" in self.structure and ('SEVERAL ANSWER OPTIONS' in self.structure or 'ANSWER OPTON' in self.structure):
            self.maxNumber = '1'
            self.minNumber = '1'
            question_type = 'ITEM_LIST_EXPANDABLE_SINGLE_CHOICE'
        # OPTION_QUESTION: S P Button
        elif 'BUTTON' in self.structure:
            question_type = 'OPTION_QUESTION'
         # SCALA_SLIDER,
        elif 'SCALA' in self.structure:
            question_type = 'SCALA_SLIDER'
            self.minNumber = self.scala_min
            self.maxNumber = self.scala_max
        # OPEN_QUESTION: S P Textfield
        elif 'ANSWER OPTION' in self.structure and not ("ITEM(Single)" or "ITEM(Multiple)") in self.structure:
            question_type = 'OPEN_QUESTION'
        elif 'Neue Etappe' in self.structure:
            question_type = 'Neue Etappe'
        elif 'ANSWER OPTIONS FROM REFERENCE (Multiple Choice)' in self.structure and not('SEVERAL ANSWER OPTIONS' in self.structure or 'ANSWER OPTION' in self.structure):
            question_type = 'ITEM_LIST_REF_CUSTOM_ANSWER_OPTIONS_NO_LIMIT'
        elif 'ANSWER OPTIONS FROM REFERENCE (Multiple Choice)' in self.structure and ('SEVERAL ANSWER OPTIONS' in self.structure or 'ANSWER OPTION' in self.structure):
            question_type = 'ITEM_LIST_MULTI_REF_CUSTOM_AND_NORMAL_EXPANDABLE_NO_LIMIT'
        elif 'ANSWER OPTIONS FROM REFERENCE (Single Choice)' in self.structure:
            question_type = 'ITEM_LIST_REF_CUSTOM_SINGLE_CHOICE'
        else:
            question_type = 'CONTENT'

        # minNumber
        if (question_type == 'ITEM_LIST_EXPANDABLE' or question_type == 'ITEM_LIST_LIMIT') and self.answer_required == 'true':
            self.minNumber = '1'

        # Warning
        if (question_type == 'ITEM_LIST_SINGLE_CHOICE') and self.answer_required == 'false':
            print('''
                    --------------------------------------------------------------------------------------------
                    |  !!!! WARNING !!!! --- Item_Single_Choice does not work with optional answer yet at question %s |
                    --------------------------------------------------------------------------------------------
                    '''%(self.excel_id))

        return question_type, self.maxNumber, self.minNumber

    def adjust_type_to_questionloop(self):
        if self.qloop_start:
            if self.type == 'ITEM_LIST_SINGLE_CHOICE':
                self.type = 'ITEM_LIST_SINGLE_CHOICE_INTERRUPTIBLE_START'
            else:
                raise Exception ('There is no question loop start screen type which is possible for the following type needed: ', self.type, ' at question: ', self.excel_id)
    

    def clear_of_nan(self):
        test_for_text_without_structure(self)
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
            scala_text = self.texts[np.where(self.structure == 'SCALA')][0]
            scala_pattern = "(\d+)\(([^)]+)\)-(\d+)\(([^)]+)\)"
            matches = re.match(scala_pattern, scala_text)
            # get variables
            self.scala_min = int(matches.group(1))
            self.scala_max = int(matches.group(3))
            self.scala_min_text = matches.group(2)
            self.scala_max_text = matches.group(4)

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
                test_for_correct_key_insight(self, self.texts[np.where(self.structure == 'KEY INSIGHT (optional)')][0])
                self.worldObjectEntryKeyType = '"'+ self.texts[np.where(self.structure == 'KEY INSIGHT (optional)')][0]+'"'
                self.optional = 'true'
            elif 'KEY INSIGHT (verpflichtend)' in self.structure:
                test_for_correct_key_insight(self, self.texts[np.where(self.structure == 'KEY INSIGHT (verpflichtend)')][0])
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
            "questionLoopId": %s,
            "translations": [],
            "content": [
                %s
                %s
            ],
            %s
            },''' %(self.id, self.type, self.minNumber, self.maxNumber, self.reviewable, self.progress, self.worldObjectEntryKeyType, self.optional, self.firstJourneyQuestion, self.firstSessionQuestion, self.questionLoopId, self.Content.json, self.AnswerOption.json, self.NextLogic.json)
        
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
        "questionLoops": [%s]
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
            '''%(self.questionLoops, id, order, durationMin, durationMax, id, title, id, title_en)
        
        return json