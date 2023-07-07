from helper import create_id

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
        for ref_number, struc in enumerate(self.structure):
            if struc == 'REFERENCE':
                ref_text = self.texts[ref_number]
                if 'sonst' in ref_text:
                    splits = ref_text.split('sonst')
                    count_sonst = len(splits)-1
                    if count_sonst > 1 and count_sonst_refs == 1:
                        self.type = 'REF_OPTIONAL'
                        for split in splits:
                            self.options.append(RefLogicOption(type = 'OPTION', questionId=create_id(self, split), questionContentId=ref_number+1))
                        # set text to 'null' else it will appear in worldobjectentry
                        self.texts[ref_number] = 'null'
                    elif count_sonst == 1:
                        self.type = 'REF_OPTIONAL_WITH_CONTENT'
                        self.options.append(RefLogicOption(type = 'OPTION_WITH_CONTENT_ID', questionContentId=ref_number+1, questionId=create_id(self, splits[0])))
                        self.options.append(RefLogicOption(type = 'OPTION_WITH_CONTENT_ID_SKIP', questionContentId=ref_number+1, questionId=create_id(self, splits[1])))
                        self.texts[ref_number] = 'null'
                    elif count_sonst > 1 and count_sonst_refs > 1:
                        raise Exception ('Too many "sonst" References in one question at question ',self.question.excel_id )

                
                
    def fill_in_parameters(self):
        for number, option in enumerate(self.options):
            option.id = self.id + '-refopt' + str(number+1)
            option.order = number+1
            option.questionContentId = self.id + "-" + str(option.questionContentId)
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
    def __init__(self, id = 'XY', order = 'XY', type = 'XY', questionRefLogicId = 'XY', questionContentId = 'XY', questionId = 'XY'):
        self.id = id
        self.order = order 
        self.type = type 
        self.questionRefLogicId = questionRefLogicId
        self.questionContentId = questionContentId
        self.questionId = questionId

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
                  "questionContentId": "%s",
                  "questionId": "%s",
                  "questionContentSubContentId": null,
                  "limit": null
                },''' %(self.id, self.order, self.type, self.questionRefLogicId, self.questionContentId, self.questionId)

    