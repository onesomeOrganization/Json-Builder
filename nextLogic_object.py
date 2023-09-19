
from helper import create_id, get_content_length, add_quotation_mark, get_one_id_higher, create_excel_id, create_condition_dict, nextLogic_patterns, get_number_and_type_for_value_option
import numpy as np
from tests import test_if_any_scala_condition_is_missing, test_for_escape_option_at_question_loop, test_if_key_ref_exists
import re

class NextLogic():
    def __init__(self, question): 
        # Attributes
        self.question = question
        self.id = question.id
        self.version = question.version
        self.id_base = question.id_base
        self.type = 'NEXT'
        self.refQuestionId = 'null'
        self.RefLogic = question.RefLogic
        self.structure = question.structure
        self.texts = question.texts
        self.reference_of_next_question = question.reference_of_next_question
        self.content_length = get_content_length(self.structure)
        self.id_next_question = self.calc_id_next_question()

        # Preparations
        self.check_for_arrows_everywhere()
        self.NextLogicOptions = []
        # different Nextlogic types:
        self.prepare_ref_key_insight()
        self.prepare_next_option_button()
        self.prepare_next_option_item()
        # self.prepare_value() Note: Value wird nicht mehr gebraucht, das Ref_Value seine funktionalität ersetzt (funktion ist aber noch drin der vollständigkeitshalber)
        self.prepare_ref_value()
        self.prepare_ref_option()
        self.prepare_ref_count()


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

    def check_for_arrows_everywhere(self):
       # infer arrows with the next screen if there are no
        exist_arrows = []
        for num, struc in enumerate(self.structure):
          if (self.question.type == 'ITEM_LIST_SINGLE_CHOICE' or self.question.type == 'ITEM_LIST_SINGLE_CHOICE_INTERRUPTIBLE_START') and struc == 'ITEM(Single)':
            if '->' in self.texts[num]:
              exist_arrows.append([True,num])
            else:
              exist_arrows.append([False, num])
        if any(item[0] for item in exist_arrows):
          for tuple in exist_arrows:
               if tuple[0] == False:
                self.texts[tuple[1]] = self.texts[tuple[1]] + '->' + create_excel_id(self.id_next_question)
        test_for_escape_option_at_question_loop(exist_arrows, self)

    # NEXT LOGIC TYPES

    def prepare_ref_key_insight(self):
    # add next question references
        # --- CONDITION ---
        for x, struct in enumerate(self.question.next_question_structure):
            # check if structure has reference
            if struct == 'REFERENCE':
                # check if key insight reference
                if self.question.next_question_texts[x].isupper():
                    # --- TYPE ---
                    self.type = 'REF_KEY_INSIGHT'
                    # --- OPTION ---
                    # add to question before
                    self.reference_of_next_question = self.question.next_question_texts[x]
                    plus_one = int(self.id_next_question[-2])+1
                    id_base_skip_question = self.id_next_question[:-2] + str(plus_one) + '"'
                    self.NextLogicOptions.append(NextLogicRefkeyOption(self.id, self.reference_of_next_question, self.id_next_question, id_base_skip_question))

    def prepare_next_option_button(self):
        # buttons
        count = 1
        for num, struc in enumerate(self.structure):
            # --- CONDITION ---
            if struc == 'BUTTON':
                if self.type != 'NEXT':
                    print('''
                    ----------------------------------------------------------------------------------------
                    |  !!!! WARNING !!!! -------- %s und Option Question gemeinsam |
                    ----------------------------------------------------------------------------------------
                    '''%(self.type))
                # --- TYPE ---
                self.type = 'NEXT_OPTION'
                # --- OPTION ---
                self.id_next_question = 'null'
                questionId = create_id(self, self.texts[num].split('->')[1])
                questionAnswerOptionId = self.id+'-'+str(self.content_length)+'-'+str(count)
                count += 1
                self.NextLogicOptions.append(NextLogicOption(self.id, num, questionId, add_quotation_mark(questionAnswerOptionId))) 
                
    
    def prepare_next_option_item(self):
        # next option items with ->
        count = 1
        for num, struc in enumerate(self.structure):
            # --- CONDITION ---
            if (struc == 'ITEM(Single)' and '->' in self.texts[num]) or (struc == 'ITEM(Multiple)' and '->' in self.texts[num] and self.question.maxNumber == '1'):
                if self.type != 'NEXT':
                    print('''
                    ----------------------------------------------------------------------------------------
                    |  !!!! WARNING !!!! -------- %s und Next Option Item gemeinsam |
                    ----------------------------------------------------------------------------------------
                    '''%(self.type))
                # --- TYPE ---
                self.type = 'NEXT_OPTION'
                # --- OPTION ---
                self.id_next_question = 'null'
                questionId = create_id(self, self.texts[num].split('->')[1])
                questionAnswerOptionId = self.id+'-'+str(self.content_length)+'-'+str(count)
                count +=1
                self.NextLogicOptions.append(NextLogicOption(self.id, num, questionId, add_quotation_mark(questionAnswerOptionId))) 


    def prepare_value(self):
        # scala and next screen depending on scala value
        for num, struc in enumerate(self.structure):
            # --- CONDITION ---
            if struc == 'weiter mit Screen' and re.match(nextLogic_patterns['VALUE'], self.texts[num]) and not re.match(nextLogic_patterns['REF_VALUE'], self.texts[num]) and not re.match(nextLogic_patterns['REF_OPTION'], self.texts[num]) and not re.match(nextLogic_patterns['REF_COUNT'], self.texts[num]):
                if self.type != 'NEXT':
                    print('''
                    ----------------------------------------------------------------------------------------
                    |  !!!! WARNING !!!! -------- %s und Scala Value gemeinsam |
                    ----------------------------------------------------------------------------------------
                    '''%(self.type))
                # --- TYPE ---
                self.type = 'VALUE'
                # --- OPTION ---
                self.id_next_question = 'null'
                text = self.texts[np.where(self.structure == 'weiter mit Screen')][0]
                scala_condition_dict = create_condition_dict(text, self.type)
                # condition: 3.10 (wenn scala = 0) 3.11 (wenn scala = 1,2,3) 3.12 (wenn Scala >= 4)
                # output: '3.10': ['=', [0]], '3.11': ['=', [1,2,3]], '3.12': ['>=', [4]] -> text hast to be stripped
                test_if_any_scala_condition_is_missing(self, scala_condition_dict)
                for num, key in enumerate(scala_condition_dict):
                    test_if_key_ref_exists(key, self.question)
                    questionId = create_id(self,key)
                    sign = scala_condition_dict[key][0]
                    values = scala_condition_dict[key][1]
                    scala_min = int(self.question.scala_min)
                    scala_max = int(self.question.scala_max)
                    type, number, secondNumber = get_number_and_type_for_value_option(scala_min, scala_max, sign, values)
                    self.NextLogicOptions.append(NextLogicOption(self.id, num, questionId, type = type, number= number, secondNumber= secondNumber))

    def prepare_ref_value(self):
        # two cases:
        # 1.4 (wenn 1.3 > 1.1)
        # 1.4 (wenn 1.1 > 2)
        # next question depending on value comparison of two scalas or the value of another previous scala
        for num, struc in enumerate(self.structure):
            # --- CONDITION ---
            if struc == 'weiter mit Screen' and re.match(nextLogic_patterns['REF_VALUE'], self.texts[num]):
                if self.type != 'NEXT' and self.type != 'REF_OPTION':
                    print('''
                    ----------------------------------------------------------------------------------------
                    |  !!!! WARNING !!!! -------- %s und Ref Value gemeinsam |
                    ----------------------------------------------------------------------------------------
                    '''%(self.type))

                condition = self.texts[num]
                count_condition_dict = create_condition_dict(condition, 'REF_VALUE')
                # test difference to ref_option:
                # Referenced question has to be a scala slider
                # option A
                for q in self.question.questions_before:
                    if list(count_condition_dict.values())[0][0] == q.excel_id:
                        if q.type != 'SCALA_SLIDER':
                            return
                        else:
                            scala_min = int(q.scala_min)
                            scala_max = int(q.scala_max)
                # Option B
                if list(count_condition_dict.values())[0][0] == self.question.excel_id or list(count_condition_dict.values())[0][0] == 'scala' or list(count_condition_dict.values())[0][0] == 'Scala':
                    if self.question.type != 'SCALA_SLIDER':
                        return
                    else:
                        scala_min = int(self.question.scala_min)
                        scala_max = int(self.question.scala_max)
                # --- TYPE ---
                self.type = 'REF_VALUE'
                # --- OPTION ---
                self.id_next_question = 'null'
                # Condition: "1.4 (wenn 1.3 > 1.1) 1.5 (wenn 1.3 < 1.1)" oder " 1.4 (wenn 1.3 > 3)" oder "1.4 (wenn 1.3 = 1,2,3)"
                # Output: '1.4': ['1.3', '>', '1.1', true], '1.5': ['1.3', '<', '1.1', true]
                count = 1
                for key in count_condition_dict:
                    test_if_key_ref_exists(key, self.question)
                    questionId = create_id(self, key)
                    sign = count_condition_dict[key][1]
                    if count_condition_dict[key][3]:
                        self.refQuestionId = add_quotation_mark(self.id)
                        if len(count_condition_dict) < 3:
                            raise Exception ('Too few conditions at question: ', self.question.excel_id)
                        if sign == '<':
                            type = 'REF_VALUE_GT'
                        elif sign == '>':
                            type = 'REF_VALUE_LT'
                        elif sign == '=':
                            type = 'REF_VALUE_E'
                        elif sign == '=' or sign == '>=' or sign == '<=':
                            raise Exception ('Count condition has a sign ("%s") which is not allowed. Question: %s (Only < and > and = are possible here)' %(sign, self.question.excel_id)) 
                        option_refQuestionId = add_quotation_mark(create_id(self, count_condition_dict[key][2][0]))
                        self.NextLogicOptions.append(NextLogicOption(self.id, count, questionId, type = type, refQuestionId= option_refQuestionId))
                    else:
                        # Relict from before Json Builder 6.0, where there still was 'VALUE':
                        if count_condition_dict[key][0] == 'scala' or count_condition_dict[key][0] == 'Scala':
                            self.refQuestionId = add_quotation_mark(self.id)
                        else:
                            self.refQuestionId = add_quotation_mark(create_id(self, count_condition_dict[key][0]))
                        values = count_condition_dict[key][2]
                        type, number, secondNumber = get_number_and_type_for_value_option(scala_min, scala_max, sign, values)
                        self.NextLogicOptions.append(NextLogicOption(self.id, count, questionId, type = type, number = number, secondNumber = secondNumber))            
                    count += 1         
    
    def prepare_ref_option(self):
        # 
        # next screen depending on answer to another question
        for num, struc in enumerate(self.structure):
            # --- CONDITION ---
            if struc == 'weiter mit Screen' and re.match(nextLogic_patterns['REF_OPTION'], self.texts[num]):
                if self.type != 'NEXT' and self.type != 'REF_VALUE':
                    print('''
                    ----------------------------------------------------------------------------------------
                    |  !!!! WARNING !!!! -------- %s und Ref option gemeinsam |
                    ----------------------------------------------------------------------------------------
                    '''%(self.type))
                condition = self.texts[num]
                # condition: 1.5 (wenn 1.2 = A) 1.6 (wenn 1.2 = B oder C)
                # output: '1.5': ['1.2, ['A']], '1.6': ['1.2, ['B','C']]   
                condition_dict = create_condition_dict(condition, 'REF_OPTION')
                # test difference to ref_value:
                for q in self.question.questions_before: 
                    if list(condition_dict.values())[0][0] == q.excel_id:
                        if q.type == 'SCALA_SLIDER':
                            return
                # --- TYPE ---
                self.type = 'REF_OPTION'
                # --- OPTION ---
                self.id_next_question = 'null'
                conditions_length = 0
                for cond in condition_dict.values():
                    conditions_length += len(cond[1])
                count = 1
                for key in condition_dict:
                    test_if_key_ref_exists(key, self.question)
                    questionId = create_id(self, key)
                    refQuestionId =  add_quotation_mark((create_id(self, condition_dict[key][0])))
                    if self.refQuestionId == 'null' or self.refQuestionId == refQuestionId:
                        self.refQuestionId = refQuestionId
                    else:
                        raise Exception ('Different refquestionIds in the condition of question: ', self.question.excel_id)
                    for question in self.question.questions_before:
                        if question.excel_id == condition_dict[key][0]:
                            #if len(question.AnswerOption.options) != conditions_length:
                                #raise Exception('Conditions are incomplete at question: ', self.question.excel_id)
                            for possible_answer in condition_dict[key][1]:
                                found = False
                                for option in question.AnswerOption.options:
                                    if option.text == possible_answer:
                                        found = True
                                        questionAnswerOptionId = option.id
                                        self.NextLogicOptions.append(NextLogicOption(self.id, count, questionId, add_quotation_mark(questionAnswerOptionId)))
                                        count += 1
                                if not found:
                                    raise Exception ('missspelling in condition of question: ', self.question.excel_id, ' for condition text: ', possible_answer)

    def prepare_ref_count(self):
        # next question depending on the count of answers of another question
        for num, struc in enumerate(self.structure):
            # --- CONDITION ---
            if struc == 'weiter mit Screen' and re.match(nextLogic_patterns['REF_COUNT'], self.texts[num]):
                if self.type != 'NEXT':
                    print('''
                    ----------------------------------------------------------------------------------------
                    |  !!!! WARNING !!!! -------- %s und Ref Count gemeinsam |
                    ----------------------------------------------------------------------------------------
                    '''%(self.type))
                # --- TYPE ---
                self.type = 'REF_COUNT'
                # --- OPTION ---
                self.id_next_question = 'null'
                condition = self.texts[num]
                # Condition: "1.2 (wenn 1.1 < 1 Antworten) 1.3 (wenn 1.1 >= 1 Antworten)"
                # Output: '1.2': ['1.1, '<', 1], '1.3': ['1.1, '>=', 1]
                count_condition_dict = create_condition_dict(condition, self.type)
                count = 1
                for key in count_condition_dict:
                    test_if_key_ref_exists(key, self.question)
                    self.refQuestionId = add_quotation_mark(create_id(self, count_condition_dict[key][0]))
                    questionId = create_id(self, key)
                    sign = count_condition_dict[key][1]
                    number = count_condition_dict[key][2]
                    if sign == '<':
                        type = 'COUNT_LT'
                    elif sign == '>=':
                        type = 'COUNT_GTE'
                    elif sign == '=' or sign == '>' or sign == '<=':
                        raise Exception ('Count condition has a sign ("%s") which is not allowed. Question: %s (Only < and >= are possible here)' %(sign, self.question.excel_id)) 
                    
                    self.NextLogicOptions.append(NextLogicOption(self.id, count, questionId, type = type, number= number))
                    count += 1

   
                

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
    def __init__(self, id, count, questionId, questionAnswerOptionId = 'null', type = 'NEXT', number = 'null', secondNumber = 'null', refQuestionId = 'null'):
        self.id = id+'-opt'+str(count)
        self.questionId = questionId
        self.questionAnswerOptionId = questionAnswerOptionId
        self.type = add_quotation_mark(type)
        self.number = number
        self.secondNumber = secondNumber
        self.refQuestionId = refQuestionId

        self.json = self.create_json()
        
    def create_json(self):
        json = '''
                {
                "id": "%s",
                "order": null,
                "type": %s,
                "number": %s,
                "count": null,
                "secondNumber": %s,
                "secondCount": null,
                "questionAnswerOptionId": %s,
                "secondQuestionAnswerOptionId": null,
                "questionId": "%s",
                "refQuestionId": %s
              },''' %(self.id, self.type, self.number, self.secondNumber, self.questionAnswerOptionId, self.questionId, self.refQuestionId)
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
    