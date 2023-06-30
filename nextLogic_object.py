
from helper import create_id, get_content_length, get_one_id_higher
import numpy as np

class NextLogic():
    def __init__(self, question): 
        # Attributes
        self.question = question
        self.id = question.id
        self.version = question.version
        self.id_base = question.id_base
        self.type = 'NEXT'
        self.options_string = ''
        self.option_screen_refs = []
        self.RefLogic = question.RefLogic
        self.structure = question.structure
        self.texts = question.texts
        self.id_next_question = self.calc_id_next_question()
        self.reference_of_next_question = question.reference_of_next_question
        self.content_length = get_content_length(self.structure)

        # Preparations
        self.prepare_button()
        self.add_arrow_logics()
        # Options
        self.NextLogicOptions = []
        self.create_options()
        # Json
        self.json = self.create_json()
        
    # -------- PREPARATIONS ------------

    def calc_id_next_question(self):
        self.id_next_question = '"'+get_one_id_higher(self.id)+'"'
        # weiter mit Screen id
        if 'weiter mit Screen' in self.structure:
            self.id_next_question = '"'+create_id(self, self.texts[np.where(self.structure == 'weiter mit Screen')][0])+'"'
        # letzter screen id_next_question = null
        elif 'letzter Screen' in self.structure:
            self.id_next_question = 'null'
        elif all(element == 'None' for element in self.question.next_question_structure):
            self.id_next_question = 'null'
        elif any(element == 'Neue Etappe' for element in self.question.next_question_structure):
            self.id_next_question = 'null'
        return self.id_next_question
    
    def add_arrow_logics(self):
        # next option items with ->
        for num, struc in enumerate(self.structure):
            if struc == 'ITEM(Single)' and '->' in self.texts[num]:
                self.options_string += 'N'
                self.type = 'NEXT_OPTION'
                self.option_screen_refs.append(create_id(self, self.texts[num].split('->')[1]))
                self.id_next_question = 'null'

    def check_for_ref_key_insight_reflogic(self):
    # add next question references
        for x, struct in enumerate(self.question.next_question_structure):
            # check if structure has reference
            if struct == 'REFERENCE':
                # check if key insight reference
                if self.question.next_question_texts[x].isupper():
                    # add to question before
                    self.reference_of_next_question = self.question.next_question_texts[x]
                    self.type = 'REF_KEY_INSIGHT'

    def prepare_button(self):
        # buttons
        if 'BUTTON' in self.structure:
            self.type = 'NEXT_OPTION'
            self.options_string = 'NN'
            # Test -> for buttons
            button_texts = self.texts[np.where(self.structure == 'BUTTON')]
            for button_text in button_texts:
                if not '->' in button_text:
                    raise Exception ('"->" missing at one of the Buttons')
            button_one = button_texts[0].split('->')
            button_two = button_texts[1].split('->')
            self.option_screen_refs.append(create_id(self, button_one[1]))
            self.option_screen_refs.append(create_id(self, button_two[1]))
            self.id_next_question = 'null'

    # ----------- CREATE OPTIONS ---------------

    def create_options(self):
        # for key insights
        if self.type == 'REF_KEY_INSIGHT': #wird in prepare_button überschrieben weil unklar ist, was mehr gilt
            plus_one = int(self.id_next_question[-2])+1
            id_base_skip_question = self.id_next_question[:-2] + str(plus_one) + '"'
            self.NextLogicOptions.append(NextLogicRefkeyOption(self.id, self.reference_of_next_question, self.id_next_question, id_base_skip_question))
        count = 1
        for number in range(len(self.options_string)):
            self.NextLogicOptions.append(NextLogicOption(self.id, count, self.content_length, self.option_screen_refs[number])) 
            count+=1

    # ----------- CREATE JSON ----------------

    def create_json(self):
        if self.RefLogic.type is None:
            questionRefLogicId = 'null'
        elif self.RefLogic.type == 'REF_OPTIONAL' or self.RefLogic.type == 'REF_AGGREGATION_ANSWER_OPTION_REF':
            questionRefLogicId = '"'+self.id+'"'

        options_json = ''
        for option in self.NextLogicOptions:
            options_json += option.json
        options_json = options_json[:-1]

        json = '''"nextLogic": {
            "id": "%s",
            "type": "%s",
            "count": null,
            "nextQuestionId": %s,
            "prevQuestionId": null,
            "refQuestionId": null,
            "questionRefLogicId": %s,
            "sessionId": null,
            %s
            "options": [
            %s
            ],
            "refAdaptions": []
          }'''%(self.id, self.type, self.id_next_question, questionRefLogicId, self.RefLogic.json, options_json) 
        return json


class NextLogicOption():
    def __init__(self, id, count, content_length, option_screen_refs):
        self.id = id+'-opt'+str(count)
        self.questionAnswerOptionId = id+'-'+str(content_length+2)+'-'+str(count) # +2 wegen answer_option & subtitel
        self.questionId = option_screen_refs

        self.json = self.create_json()
        
    def create_json(self):
        json = '''
                {
                "id": "%s",
                "order": null,
                "type": "NEXT",
                "number": null,
                "count": null,
                "secondNumber": null,
                "secondCount": null,
                "questionAnswerOptionId": "%s",
                "secondQuestionAnswerOptionId": null,
                "questionId": "%s",
                "refQuestionId": null
              },''' %(self.id, self.questionAnswerOptionId, self.questionId)
        return json
    
class NextLogicRefkeyOption():
    def __init__(self, id, reference_of_next_question, id_base_next_question, id_base_skip_question):
        self.id = id
        self.id_base_next_question = id_base_next_question
        self.id_base_skip_question = id_base_skip_question
        self.worldObjectEntryKey  = reference_of_next_question
        self.json = self.create_json()

    def create_json(self):
        json = '''
                {
                "id": "%s-opt1",
                "order": 1,
                "type": "NEXT",
                "number": null,
                "count": null,
                "secondNumber": null,
                "secondCount": null,
                "questionAnswerOptionId": null,
                "secondQuestionAnswerOptionId": null,
                "questionId": %s,
                "refQuestionId": null
              },
              {
                "id": "%s-opt2",
                "order": 2,
                "type": "NEXT",
                "number": null,
                "count": null,
                "secondNumber": null,
                "secondCount": null,
                "questionAnswerOptionId": null,
                "secondQuestionAnswerOptionId": null,
                "questionId": %s,
                "refQuestionId": null
              },
              {
                "id": "%s-opt3",
                "order": 3,
                "type": "REF_KEY_INSIGHT_GENERATE",
                "number": null,
                "count": null,
                "secondNumber": null,
                "secondCount": null,
                "questionAnswerOptionId": null,
                "secondQuestionAnswerOptionId": null,
                "questionId": %s,
                "worldObjectEntryKey": "%s",
                "refQuestionId": null
              },''' %(self.id, self.id_base_next_question, self.id, self.id_base_skip_question ,self.id, self.id_base_next_question, self.worldObjectEntryKey)
        return json
    