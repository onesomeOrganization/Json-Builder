
from helper import create_id, get_content_length, get_one_id_higher, delete_last_number_from_id, add_quotation_mark, extract_values_from_wenn_condition
import numpy as np
import re

class NextLogic():
    def __init__(self, question): 
        # Attributes
        self.question = question
        self.id = question.id
        self.version = question.version
        self.id_base = question.id_base
        self.type = 'NEXT'
        #self.options_string = ''
        self.refQuestionId = 'null'
        #self.option_screen_refs = []
        self.RefLogic = question.RefLogic
        self.structure = question.structure
        self.texts = question.texts
        self.id_next_question = self.calc_id_next_question()
        self.reference_of_next_question = question.reference_of_next_question
        self.content_length = get_content_length(self.structure)

        # Preparations
        self.NextLogicOptions = []
        self.prepare_ref_key_insight()
        self.prepare_next_option_button()
        self.prepare_next_option_item()
        self.prepare_ref_option()

        # Json
        self.json = self.create_json()
        
    # -------- PREPARATIONS ------------
    def calc_id_next_question(self):
        self.id_next_question = add_quotation_mark(get_one_id_higher(self.id))
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

    def prepare_ref_key_insight(self):
    # add next question references
        for x, struct in enumerate(self.question.next_question_structure):
            # check if structure has reference
            if struct == 'REFERENCE':
                # check if key insight reference
                if self.question.next_question_texts[x].isupper():
                    # add to question before
                    self.reference_of_next_question = self.question.next_question_texts[x]
                    self.type = 'REF_KEY_INSIGHT'
                    plus_one = int(self.id_next_question[-2])+1
                    id_base_skip_question = self.id_next_question[:-2] + str(plus_one) + '"'
                    self.NextLogicOptions.append(NextLogicRefkeyOption(self.id, self.reference_of_next_question, self.id_next_question, id_base_skip_question))

    def prepare_next_option_button(self):
        # buttons
        count = 1
        for num, struc in enumerate(self.structure):
            if struc == 'BUTTON':
                if self.type == 'REF_KEY_INSIGHT':
                    print('''
                    ----------------------------------------------------------------------------------------
                    |  !!!! WARNING !!!! -------- Schlüsselerkenntnisreferenz und Option Question gemeinsam |
                    ----------------------------------------------------------------------------------------
                    ''')
                self.type = 'NEXT_OPTION'
                self.id_next_question = 'null'
                questionId = create_id(self, self.texts[num].split('->')[1])
                questionAnswerOptionId = self.id+'-'+str(self.content_length+2)+'-'+str(count)
                count += 1
                self.NextLogicOptions.append(NextLogicOption(self.id, num, questionId, questionAnswerOptionId)) 
                
    
    
    def prepare_next_option_item(self):
        # next option items with ->
        count = 1
        for num, struc in enumerate(self.structure):
            if (struc == 'ITEM(Single)' and '->' in self.texts[num]) or (struc == 'ITEM(Multiple)' and '->' in self.texts[num] and self.question.maxNumber == '1'):
                if self.type == 'REF_KEY_INSIGHT':
                    print('''
                    ---------------------------------------------------------------------------------------------
                    |  !!!! WARNING !!!! -------- Schlüsselerkenntnisreferenz und Arrow Logic mit Item gemeinsam |
                    ---------------------------------------------------------------------------------------------
                    ''')
                self.type = 'NEXT_OPTION'
                self.id_next_question = 'null'
                questionId = create_id(self, self.texts[num].split('->')[1])
                questionAnswerOptionId = self.id+'-'+str(self.content_length+2)+'-'+str(count)
                count +=1
                self.NextLogicOptions.append(NextLogicOption(self.id, num, questionId, questionAnswerOptionId)) 

    
    def prepare_ref_option(self):
        # WARNING: hier ist bereits alles implementiert dass die ref_option auch mit button und items geht (auch bei der adjazenzliste von progress)
        # button oder item + -> und (wenn
        for num, struc in enumerate(self.structure):
            if (struc == 'ITEM(Single)' or (struc == 'ITEM(Multiple)' and self.question.maxNumber == '1') or struc == 'BUTTON' or struc == 'weiter mit Screen') and ('(wenn' in self.texts[num]):
                if self.type == 'REF_KEY_INSIGHT':
                    print('''
                    ---------------------------------------------------------------------------------------------------
                    |  !!!! WARNING !!!! --- Schlüsselerkenntnisreferenz und Arrow Logic mit wenn in Item gemeinsam    |
                    ---------------------------------------------------------------------------------------------------
                    ''')
                self.type = 'REF_OPTION'
                self.id_next_question = 'null'
                if struc == 'weiter mit Screen':
                    condition = self.texts[num]
                else:
                    raise Exception ('REF_OPTION und NEXT_OPTION gleichzeitig nötig, da wenn condition und button/item in frage ', self.question.excel_id)
                    condition = self.texts[num].split('->')[1]
                condition_dict = extract_values_from_wenn_condition(condition)
                for key in condition_dict:
                    questionId = create_id(self, key)
                    self.refQuestionId =  add_quotation_mark((create_id(self, condition_dict[key][0])))
                    for question in self.question.questions_before:
                        if question.excel_id == condition_dict[key][0]:
                            for option in question.AnswerOption.options:
                                for possible_answer in condition_dict[key][1]:
                                    if option.text == possible_answer:
                                        questionAnswerOptionId = option.id
                                        self.NextLogicOptions.append(NextLogicOption(self.id, num, questionId, questionAnswerOptionId)) 
                # TODO: test if all options are occupied with a screen

    # ----------- CREATE JSON ----------------

    def create_json(self):
        if self.RefLogic.type is None:
            questionRefLogicId = 'null'
        elif self.RefLogic.type == 'REF_OPTIONAL' or self.RefLogic.type == 'REF_OPTIONAL_WITH_CONTENT':
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
            "refQuestionId": %s,
            "questionRefLogicId": %s,
            "sessionId": null,
            %s
            "options": [
            %s
            ],
            "refAdaptions": []
          }'''%(self.id, self.type, self.id_next_question, self.refQuestionId, questionRefLogicId, self.RefLogic.json, options_json) 
        return json


class NextLogicOption():
    def __init__(self, id, count, questionId, questionAnswerOptionId):
        self.id = id+'-opt'+str(count)
        self.questionId = questionId
        self.questionAnswerOptionId = questionAnswerOptionId

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
    