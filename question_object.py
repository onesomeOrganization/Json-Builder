import numpy as np
import re
from refLogic_functions import *
from content_block_functions import Content
from answer_option_functions import *
from nextLogic_functions import *
from helper import create_id, get_content_length



# TODO: Answer options 
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
    def __init__(self, id_base, version, structure, texts, next_question_structure, next_question_texts, excel_id, write_beginning, write_ending):
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

        # PREPARATIONS
        self.clear_of_nan()
        self.solve_answer_problem()
        self.type = self.map_structure_to_type() 
        self.answer_required = self.prepare_optional()
        self.scala_min, self.scala_max, self.scala_min_text, self.scala_max_text = self.prepare_scala()
        
        # TODO clean
        self.prepare_keyInsight()
        self.answer_option = map_structure_to_answer_option(self.structure, self.type)
        

        # BUILDING BLOCKS
        self.id_next_question = self.calc_id_next_question()
        self.check_for_ref_key_insight_reflogic()
        self.RefLogic = RefLogic(self.structure, self.texts, self.id_base, self.version, id=self.id)
        self.NextLogic = NextLogic(self.id, self.id_base, self.version, self.RefLogic, self.structure, self.texts, self.id_next_question, self.reference_of_next_question, self.next_logic_type)
        self.prepare_for_content()
        self.Content = Content(self.id, self.structure, self.texts)
    
    def check_for_ref_key_insight_reflogic(self):
    # add next question references
        for x, struct in enumerate(self.next_question_structure):
            # check if structure has reference
            if struct == 'REFERENCE':
                # check if key insight reference
                if self.next_question_texts[x].isupper():
                    # add to question before
                    self.reference_of_next_question = self.next_question_texts[x]
                    self.next_logic_type = 'REF_KEY_INSIGHT'

    def prepare_for_content(self):
        # arrow logics
        for num, struc in enumerate(self.structure):
            if struc == 'ITEM(Single)' and '->' in self.texts[num]:
                self.texts[num] = self.texts[num].split('->')[0].strip()
        # button logics
        if 'BUTTON' in self.structure:
            # Test -> for buttons
            button_texts = self.texts[np.where(self.structure == 'BUTTON')]
            for button_text in button_texts:
                if not '->' in button_text:
                    raise Exception ('"->" missing at one of the Buttons')
            button_one = button_texts[0].split('->')
            button_two = button_texts[1].split('->')
            self.button_one_text = button_one[0].strip()
            self.button_two_text = button_two[0].strip()


    def calc_id_next_question(self):
        id_next_question = '"'+self.id_base+self.version+"-"+self.etappe+"-"+str(int(self.screen)+1)+'"'
        # weiter mit Screen id
        if 'weiter mit Screen' in self.structure:
            id_next_question = '"'+create_id(self, self.texts[np.where(self.structure == 'weiter mit Screen')][0])+'"'
        # letzter screen id_next_question = null
        elif 'letzter Screen' in self.structure:
            id_next_question = 'null'
        # next question neue etappe or last question in array: null
        #if i == (len(questions_array)-1) or (i < (len(questions_array)-1) and questions_array[i+1].type == 'Neue Etappe'):
        #    id_next_question = 'null'
        return id_next_question

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

    def create_json(self):
        content_length = get_content_length(self.structure)+2 # fragen fangen nicht von 0 an und Subititel 
        question = self
        count = self.screen
        texts = question.texts
        write_beginning = self.write_beginning
        if self.type == 'CONTENT':
            json = ''' 
            {
            "id": "%s",
            "type": "CONTENT",
            "number": null,
            "minNumber": null,
            "maxNumber": null,
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
                {
                "id": "%s-1",
                "type": "SUB_TITLE",
                "required": null,
                "showHidden": null,
                "order": 1,
                "imageName": null,
                "audioName": null,
                "style": null,
                "refAdaptionType": null,
                "refAdaptionNumber": null,
                "refOrderType": null,
                "refOrderColumn": null,
                "refOffset": null,
                "refLimit": null,
                "downloadName": null,
                "checkForSpecialTextReplacement": null,
                "questionAnswerOptionId": null,
                "language": null,
                "contentShowType": null,
                "worldObjectEntryKey": null,
                "refQuestionId": null,
                "refQuestionAnswerOptionId": null,
                "translations": [
                    {
                    "id": "%s-1-DE",
                    "language": "DE",
                    "title": null,
                    "text": "%s"
                    },
                    {
                    "id": "%s-1-EN",
                    "language": "EN",
                    "title": null,
                    "text": "Englisch"
                    }
                ],
                "answerOptions": []
                }%s
            ],
            %s
            },''' % (question.id, question.reviewable, question.progress, question.worldObjectEntryKeyType, question.optional, "true" if count == 0 and self.write_beginning == True else "null", "true" if count == 0 and self.write_beginning == True else "null", question.id, question.id, self.texts[0], question.id, self.Content.json, self.NextLogic.json)
        elif self.type == 'OPTION_QUESTION':
            json = '''
            {
            "id": "%s",
            "type": "OPTION_QUESTION",
            "number": null,
            "minNumber": null,
            "maxNumber": null,
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
                {
                "id": "%s-1",
                "type": "SUB_TITLE",
                "required": null,
                "showHidden": null,
                "order": 1,
                "imageName": null,
                "audioName": null,
                "style": null,
                "refAdaptionType": null,
                "refAdaptionNumber": null,
                "refOrderType": null,
                "refOrderColumn": null,
                "refOffset": null,
                "refLimit": null,
                "downloadName": null,
                "checkForSpecialTextReplacement": null,
                "questionAnswerOptionId": null,
                "language": null,
                "contentShowType": null,
                "worldObjectEntryKey": null,
                "refQuestionId": null,
                "refQuestionAnswerOptionId": null,
                "translations": [
                    {
                    "id": "%s-1-DE",
                    "language": "DE",
                    "title": null,
                    "text": "%s"
                    },
                    {
                    "id": "%s-1-EN",
                    "language": "EN",
                    "title": "",
                    "text": "Englisch"
                    }
                ],
                "answerOptions": []
                }%s
                ,{
                "id": "%s-%s",
                "type": "ANSWER_OPTION",
                "required": true,
                "showHidden": null,
                "order": %s,
                "imageName": null,
                "audioName": null,
                "style": null,
                "refAdaptionType": null,
                "refAdaptionNumber": null,
                "refOrderType": null,
                "refOrderColumn": null,
                "refOffset": null,
                "refLimit": null,
                "downloadName": null,
                "checkForSpecialTextReplacement": null,
                "questionAnswerOptionId": null,
                "language": null,
                "contentShowType": null,
                "worldObjectEntryKey": null,
                "refQuestionId": null,
                "refQuestionAnswerOptionId": null,
                "translations": [],
                "answerOptions": [
                    {
                    "id": "%s-%s-1",
                    "order": 1,
                    "number": null,
                    "type": "BUTTON",
                    "imageName": null,
                    "hidden": null,
                    "escapeOption": null,
                    "sliderType": null,
                    "negative": null,
                    "unselectOthers": null,
                    "booleanHelper": null,
                    "refQuestionAnswerOptionId": null,
                    "secondRefQuestionAnswerOptionId": null,
                    "questionLoopCycleId": null,
                    "translations": [
                        {
                        "id": "%s-%s-1-DE",
                        "language": "DE",
                        "title": null,
                        "text": "%s",
                        "description": ""
                        },
                        {
                        "id": "%s-%s-1-EN",
                        "language": "EN",
                        "title": "",
                        "text": "Englisch",
                        "description": ""
                        }
                    ]
                    },
                    {
                    "id": "%s-%s-2",
                    "order": 2,
                    "number": null,
                    "type": "BUTTON",
                    "imageName": null,
                    "hidden": null,
                    "escapeOption": null,
                    "sliderType": null,
                    "negative": null,
                    "unselectOthers": null,
                    "booleanHelper": null,
                    "refQuestionAnswerOptionId": null,
                    "secondRefQuestionAnswerOptionId": null,
                    "questionLoopCycleId": null,
                    "translations": [
                        {
                        "id": "%s-%s-2-DE",
                        "language": "DE",
                        "title": null,
                        "text": "%s",
                        "description": ""
                        },
                        {
                        "id": "%s-%s-2-EN",
                        "language": "EN",
                        "title": "",
                        "text": "Englisch",
                        "description": ""
                        }
                    ]
                    }
                ]
                }
            ],
            %s
            },'''% (question.id, question.reviewable, question.progress, question.worldObjectEntryKeyType, question.optional, "true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and self.write_beginning == True else "null", question.id, question.id, self.texts[0], question.id, self.Content.json,question.id, content_length, content_length, question.id, content_length, question.id, content_length, question.button_one_text, question.id, content_length, question.id, content_length, question.id, content_length, question.button_two_text, question.id, content_length, self.NextLogic.json)
        elif self.type == 'OPEN_QUESTION':
            json = '''
            {
            "id": "%s",
            "type": "OPEN_QUESTION",
            "number": null,
            "minNumber": null,
            "maxNumber": null,
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
                {
                "id": "%s-1",
                "type": "SUB_TITLE",
                "required": null,
                "showHidden": null,
                "order": 1,
                "imageName": null,
                "audioName": null,
                "style": null,
                "refAdaptionType": null,
                "refAdaptionNumber": null,
                "refOrderType": null,
                "refOrderColumn": null,
                "refOffset": null,
                "refLimit": null,
                "downloadName": null,
                "checkForSpecialTextReplacement": null,
                "questionAnswerOptionId": null,
                "language": null,
                "contentShowType": null,
                "worldObjectEntryKey": null,
                "refQuestionId": null,
                "refQuestionAnswerOptionId": null,
                "translations": [
                    {
                    "id": "%s-1-DE",
                    "language": "DE",
                    "title": null,
                    "text": "%s"
                    },
                    {
                    "id": "%s-1-EN",
                    "language": "EN",
                    "title": "",
                    "text": "Englisch"
                    }
                ],
                "answerOptions": []
                }%s     
                ,{
                "id": "%s-%s",
                "type": "ANSWER_OPTION",
                "required": %s,
                "showHidden": null,
                "order": %s,
                "imageName": null,
                "audioName": null,
                "style": null,
                "refAdaptionType": null,
                "refAdaptionNumber": null,
                "refOrderType": null,
                "refOrderColumn": null,
                "refOffset": null,
                "refLimit": null,
                "downloadName": null,
                "checkForSpecialTextReplacement": null,
                "questionAnswerOptionId": null,
                "language": null,
                "contentShowType": null,
                "worldObjectEntryKey": null,
                "refQuestionId": null,
                "refQuestionAnswerOptionId": null,
                "translations": [],
                "answerOptions": [
                    {
                    "id": "%s-%s-1",
                    "order": 1,
                    "number": null,
                    "type": "TEXT_FIELD",
                    "imageName": null,
                    "hidden": null,
                    "escapeOption": null,
                    "sliderType": null,
                    "negative": null,
                    "unselectOthers": null,
                    "booleanHelper": null,
                    "refQuestionAnswerOptionId": null,
                    "secondRefQuestionAnswerOptionId": null,
                    "questionLoopCycleId": null,
                    "translations": []
                    }
                ]
                }
            ],
            %s
            },''' % (question.id, question.reviewable, question.progress, question.worldObjectEntryKeyType, question.optional, "true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", question.id,question.id,texts[0], question.id,self.Content.json, question.id, content_length, question.answer_required, content_length, question.id, content_length, self.NextLogic.json)
        elif self.type == 'SCALA_SLIDER':
            json = '''
            {
            "id": "%s",
            "type": "SCALA_SLIDER",
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
                {
                "id": "%s-1",
                "type": "SUB_TITLE",
                "required": null,
                "showHidden": null,
                "order": 1,
                "imageName": null,
                "audioName": null,
                "style": null,
                "refAdaptionType": null,
                "refAdaptionNumber": null,
                "refOrderType": null,
                "refOrderColumn": null,
                "refOffset": null,
                "refLimit": null,
                "downloadName": null,
                "checkForSpecialTextReplacement": null,
                "questionAnswerOptionId": null,
                "language": null,
                "contentShowType": null,
                "worldObjectEntryKey": null,
                "refQuestionId": null,
                "refQuestionAnswerOptionId": null,
                "translations": [
                    {
                    "id": "%s-1-DE",
                    "language": "DE",
                    "title": null,
                    "text": "%s"
                    },
                    {
                    "id": "%s-1-EN",
                    "language": "EN",
                    "title": null,
                    "text": "Englisch"
                    }
                ],
                "answerOptions": []
                }%s
                ,{
                "id": "%s-%s",
                "type": "ANSWER_OPTION",
                "required": true,
                "showHidden": null,
                "order": %s,
                "imageName": null,
                "audioName": null,
                "style": null,
                "refAdaptionType": null,
                "refAdaptionNumber": null,
                "refOrderType": null,
                "refOrderColumn": null,
                "refOffset": null,
                "refLimit": null,
                "downloadName": null,
                "checkForSpecialTextReplacement": null,
                "questionAnswerOptionId": null,
                "language": null,
                "contentShowType": null,
                "worldObjectEntryKey": null,
                "refQuestionId": null,
                "refQuestionAnswerOptionId": null,
                "translations": [],
                "answerOptions": [
                    {
                    "id": "%s-%s-1",
                    "order": 1,
                    "number": null,
                    "type": "SLIDER",
                    "imageName": null,
                    "hidden": null,
                    "escapeOption": null,
                    "sliderType": null,
                    "negative": null,
                    "unselectOthers": null,
                    "booleanHelper": null,
                    "refQuestionAnswerOptionId": null,
                    "secondRefQuestionAnswerOptionId": null,
                    "questionLoopCycleId": null,
                    "translations": [
                        {
                        "id": "%s-%s-1-DE",
                        "language": "DE",
                        "title": null,
                        "text": "%s, ,%s",
                        "description": ""
                        },
                        {
                        "id": "%s-%s-1-EN",
                        "language": "EN",
                        "title": null,
                        "text": "Englisch",
                        "description": ""
                        }
                    ]
                    }
                ]
                }
            ],
            %s
            },''' % (question.id,question.scala_min,question.scala_max, question.reviewable, question.progress, question.worldObjectEntryKeyType, question.optional, "true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", question.id, question.id,texts[0], question.id, self.Content.json ,question.id, content_length, content_length, question.id, content_length, question.id, content_length, question.scala_min_text, question.scala_max_text,question.id, content_length, self.NextLogic.json)
        elif self.type == 'ITEM_LIST_EXPANDABLE':
            json = '''
            {
            "id": "%s",
            "type": "ITEM_LIST_EXPANDABLE",
            "number": null,
            "minNumber": 1,
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
                {
                "id": "%s-1",
                "type": "SUB_TITLE",
                "required": null,
                "showHidden": null,
                "order": 1,
                "imageName": null,
                "audioName": null,
                "style": null,
                "refAdaptionType": null,
                "refAdaptionNumber": null,
                "refOrderType": null,
                "refOrderColumn": null,
                "refOffset": null,
                "refLimit": null,
                "downloadName": null,
                "checkForSpecialTextReplacement": null,
                "questionAnswerOptionId": null,
                "language": null,
                "contentShowType": null,
                "worldObjectEntryKey": null,
                "refQuestionId": null,
                "refQuestionAnswerOptionId": null,
                "translations": [
                    {
                    "id": "%s-1-DE",
                    "language": "DE",
                    "title": null,
                    "text": "%s"
                    },
                    {
                    "id": "%s-1-EN",
                    "language": "EN",
                    "title": "",
                    "text": "Englisch"
                    }
                ],
                "answerOptions": []
                }%s
                ,{
                "id": "%s-%s",
                "type": "ANSWER_OPTION",
                "required": %s,
                "showHidden": null,
                "order": %s,
                "imageName": null,
                "audioName": null,
                "style": null,
                "refAdaptionType": null,
                "refAdaptionNumber": null,
                "refOrderType": null,
                "refOrderColumn": null,
                "refOffset": null,
                "refLimit": null,
                "downloadName": null,
                "checkForSpecialTextReplacement": null,
                "questionAnswerOptionId": null,
                "language": null,
                "contentShowType": null,
                "worldObjectEntryKey": null,
                "refQuestionId": null,
                "refQuestionAnswerOptionId": null,
                "translations": [],
                "answerOptions": [
                    %s
                ]
                }
            ],
            %s
            },''' % (question.id, question.maxNumber, question.reviewable, question.progress, question.worldObjectEntryKeyType, question.optional, "true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", question.id,question.id, texts[0], question.id,self.Content.json, question.id, content_length, question.answer_required, content_length, create_answer_options(question, question.id, content_length, self.answer_option, texts), self.NextLogic.json)
        elif self.type == 'ITEM_LIST_SINGLE_CHOICE':
            json = '''
            {
            "id": "%s",
            "type": "ITEM_LIST_SINGLE_CHOICE",
            "number": null,
            "minNumber": null,
            "maxNumber": null,
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
                {
                "id": "%s-1",
                "type": "SUB_TITLE",
                "required": null,
                "showHidden": null,
                "order": 1,
                "imageName": null,
                "audioName": null,
                "style": null,
                "refAdaptionType": null,
                "refAdaptionNumber": null,
                "refOrderType": null,
                "refOrderColumn": null,
                "refOffset": null,
                "refLimit": null,
                "downloadName": null,
                "checkForSpecialTextReplacement": null,
                "questionAnswerOptionId": null,
                "language": null,
                "contentShowType": null,
                "worldObjectEntryKey": null,
                "refQuestionId": null,
                "refQuestionAnswerOptionId": null,
                "translations": [
                    {
                    "id": "%s-1-DE",
                    "language": "DE",
                    "title": null,
                    "text": "%s"
                    },
                    {
                    "id": "%s-1-EN",
                    "language": "EN",
                    "title": null,
                    "text": "Englisch"
                    }
                ],
                "answerOptions": []
                }%s
                ,{
                "id": "%s-%s",
                "type": "ANSWER_OPTION",
                "required": true,
                "showHidden": null,
                "order": %s,
                "imageName": null,
                "audioName": null,
                "style": null,
                "refAdaptionType": null,
                "refAdaptionNumber": null,
                "refOrderType": null,
                "refOrderColumn": null,
                "refOffset": null,
                "refLimit": null,
                "checkForSpecialTextReplacement": null,
                "questionAnswerOptionId": null,
                "language": null,
                "refQuestionId": null,
                "translations": [],
                "answerOptions": [
                    %s
                ]
                }
            ],
            %s
            },'''%(question.id, question.reviewable, question.progress, question.worldObjectEntryKeyType, question.optional,"true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", question.id, question.id,texts[0], question.id, self.Content.json, question.id, content_length, content_length, create_answer_options(question, question.id, content_length, self.answer_option, texts), self.NextLogic.json    )
        elif self.type == 'Neue Etappe':
            json = '''
            ],
        "questionLoops": []
        },
        {
        "id": "%s%s-%s",
        "order": %s,
        "durationMin": %s,
        "durationMax": %s,
        "translations": [
            {
            "id": "%s%s-%s-DE",
            "language": "DE",
            "title": "%s"
            },
            {
            "id": "%s%s-%s-EN",
            "language": "EN",
            "title": "Englisch"
            }
        ],
        "questions": [
            '''%(self.id_base, self.version, self.etappe, self.etappe, int(texts[np.where(question.structure == 'Zeit min')][0]) if 'Zeit min' in question.structure else '', int(texts[np.where(question.structure == 'Zeit max')][0]) if 'Zeit max' in question.structure else '', self.id_base, self.version, self.etappe, texts[np.where(question.structure == 'Etappen-Titel')][0] if 'Zeit min' in question.structure else '',self.id_base, self.version, self.etappe)
        else:
            raise Exception ('unknown Type in create_question_json')
        return json
        
        