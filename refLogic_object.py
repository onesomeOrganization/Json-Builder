from helper import create_id, content_length_dict, add_quotation_mark, screen_reference_pattern, key_insight_pattern
import numpy as np
import re

class RefLogic:
    def __init__(self, question):
        # Attributes
        self.question = question
        self.id = question.id
        self.id_base = question.id_base
        self.version = question.version
        self.texts = question.texts
        self.structure = question.structure
        self.json = ''
        # Options
        self.type = None
        self.options = []
        self.create_type_and_options()
        # Json
        if self.type is not None:
            self.create_json()
    
    # ------ PREPARATIONS -----------

    def create_type_and_options(self):
        count_sonst_refs = 0
        # count "sonst" 
        for enum, struc in enumerate(self.structure):
            if struc == 'REFERENCE' and 'sonst' in self.texts[enum]:
                count_sonst_refs += 1
        # set reflogic option type
        ref_number = 1
        for num, struc in enumerate(self.structure):
            if struc == 'REFERENCE':
                ref_text = self.texts[num]
                if 'sonst' in ref_text:
                    splits = ref_text.split('sonst')
                    count_sonst = len(splits)-1
                    if count_sonst > 1 and count_sonst_refs == 1:
                        self.type = 'REF_OPTIONAL'
                        for split in splits:
                            self.options.append(RefLogicOption(type = 'OPTION', questionId=create_id(self, split), questionContentId=ref_number))
                        # set text to 'null' else it will appear in worldobjectentry
                        self.texts[num] = 'null'
                    elif count_sonst == 1:
                        self.type = 'REF_OPTIONAL_WITH_CONTENT'
                        # check for key insight:
                        if bool(re.match(screen_reference_pattern, splits[0].strip())):
                            questionId = create_id(self, splits[0])
                            worldObjectEntryKey = 'null'
                        elif bool(re.match(key_insight_pattern, splits[0].strip())):
                            worldObjectEntryKey = splits[0]
                            questionId = 'null'
                        else: 
                            raise Exception('First reference in (%s) from question %s is neither a proper screen-reference nor a key insight reference.'%(ref_text,  self.question.excel_id))
                        self.options.append(RefLogicOption(type = 'OPTION_WITH_CONTENT_ID', questionContentId=ref_number, questionId=questionId, worldObjectEntryKey=worldObjectEntryKey))
                        # check for key insight:
                        if bool(re.match(screen_reference_pattern, splits[1].strip())):
                            questionId = create_id(self, splits[1])
                            worldObjectEntryKey = 'null'
                        elif bool(re.match(key_insight_pattern, splits[1].strip())):
                            worldObjectEntryKey = splits[1]
                            questionId = 'null'
                        else: 
                            raise Exception('Second reference in (%s) from question %s is neither a proper screen-reference nor a key insight reference.'%(ref_text, self.question.excel_id))
                        self.options.append(RefLogicOption(type = 'OPTION_WITH_CONTENT_ID_SKIP', questionContentId=ref_number, questionId=questionId, worldObjectEntryKey=worldObjectEntryKey))
                        self.texts[num] = 'null'
                    elif count_sonst > 1 and count_sonst_refs > 1:
                        raise Exception ('Too many "sonst" References in one question at question ',self.question.excel_id )
            if struc in content_length_dict:
                ref_number += content_length_dict[struc]
        if self.question.type == 'ITEM_LIST_MULTI_REF_CUSTOM_AND_NORMAL_EXPANDABLE_NO_LIMIT':
            if self.type is not None:
                raise Exception ("A questiontype of ITEM_LIST_MULTI_REF_CUSTOM_AND_NORMAL_EXPANDABLE_NO_LIMIT (Several answer options with answer options from reference) is not possible together with reflogic %s" %(self.type))
            else:
                self.type = 'ANSWER_AGGREGATION'
                self.options.append(RefLogicOption(type = 'ANSWER_AGGREGATION',  questionRefLogicId= self.id, questionContentId='null', questionId= create_id(self, self.texts[np.where(self.structure == 'ANSWER OPTIONS FROM REFERENCE (Multiple Choice)')][0])))

                
                
    def fill_in_parameters(self):
        for number, option in enumerate(self.options):
            option.id = self.id + '-refopt' + str(number+1)
            option.order = number+1
            if option.questionContentId != 'null':
                option.questionContentId = add_quotation_mark(self.id + "-" + str(option.questionContentId))
            option.questionRefLogicId = self.id

    # ---------- JSON -------------------

    def create_json(self):
        self.fill_in_parameters()
        options_json = ''
        for num, option in enumerate(self.options):
            option.create_json()
            options_json += option.json
            if num == len(self.options)-1:
                options_json = options_json[:-1]
        self.json = '''"refLogic": {
                "id": "%s",
                "type": "%s",
                "refQuestionId": null,
                "options": [%s
                ]
            },''' %(self.id, self.type, options_json)


class RefLogicOption:
    def __init__(self, id = 'XY', order = 'XY', type = 'XY', questionRefLogicId = 'XY', questionContentId = 'XY', questionId = 'null', worldObjectEntryKey = 'null'):
        self.id = id
        self.order = order 
        self.type = type 
        self.questionRefLogicId = questionRefLogicId
        self.questionContentId = questionContentId
        self.questionId = questionId
        self.worldObjectEntryKey = worldObjectEntryKey

        if self.questionId != 'null':
            self.questionId = add_quotation_mark(self.questionId)
        if self.worldObjectEntryKey != 'null':
            self.worldObjectEntryKey = add_quotation_mark(self.worldObjectEntryKey.strip())

    def create_json(self):
        self.json = '''
                {
                  "id": "%s",
                  "order": %s,
                  "type": "%s",
                  "number": null,
                  "questionRefLogicId": "%s",
                  "questionAnswerOptionId": null,
                  "secondQuestionAnswerOptionId": null,
                  "questionContentId": %s,
                  "questionId": %s,
                  "worldObjectEntryKey": %s,
                  "questionContentSubContentId": null,
                  "limit": null
                },''' %(self.id, self.order, self.type, self.questionRefLogicId, self.questionContentId, self.questionId, self.worldObjectEntryKey)

    