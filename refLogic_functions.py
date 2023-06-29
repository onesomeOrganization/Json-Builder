from helper import create_id

class RefLogic:
    def __init__(self, structure, texts, id_base, version, id = 'XY', type = 'XY', refQuestionId = 'XY', options = []):
        self.type = type
        self.id = id
        self.refQuestionId = refQuestionId
        self.options = options
        self.id_base = id_base
        self.version = version
        self.texts = texts
        self.structure = structure
        self.json = ''
        self.create_type_and_options()
        if self.type != 'XY':
            self.create_json()

    def create_type_and_options(self):
        count_special_refs = 0
        # check for several "sonst" "und"
        for enum, struc in enumerate(self.structure):
            if struc == 'REFERENCE' and ('sonst' in self.texts[enum] or 'und' in self.texts[enum]):
                count_special_refs += 1
        # check for "sonst" und "und" in Reference and set type
        for ref_number, struc in enumerate(self.structure):
            if struc == 'REFERENCE':
                ref_text = self.texts[ref_number]
                if 'sonst' in ref_text and count_special_refs == 1:
                    # if found set self.refLogic_type to REF_OPTIONAL
                    self.type = 'REF_OPTIONAL'
                    # count how many and create options as self.refLogics
                    splits = ref_text.split('sonst')
                    for split in splits:
                        self.options.append(RefLogicOption(type = 'OPTION', questionId=create_id(self, split), questionContentId=ref_number+1))
                    # set text to '' else it will appear in worldobjectentry
                    self.texts[ref_number] = 'null'
                    mehrere = 1
                elif 'und' in ref_text:
                    # if found set self.refLogic_type to REF_AGGREGATION_ANSWER_OPTION_REF mit OPTION_WITH_CONTENT_ID
                    self.RefLogic.type = 'REF_AGGREGATION_ANSWER_OPTION_REF'
                    # count how many and create options as self.refLogics
                    splits = ref_text.split('und')
                    for split in splits:
                        # OPTION_WITH_CONTENT_ID
                        self.RefLogic.options.append(RefLogicOption(type = 'OPTION_WITH_CONTENT_ID', questionContentId=ref_number+1, questionId=create_id(self, split)))
                    # set text to '' else it will appear in worldobjectentry
                    self.texts[ref_number] = 'null'
                    mehrere = 1
                elif 'sonst' in ref_text and count_special_refs > 1:
                    # if found set self.refLogic_type to REF_AGGREGATION_ANSWER_OPTION_REF mit OPTION_WITH_CONTENT_ID
                    self.RefLogic.type= 'REF_AGGREGATION_ANSWER_OPTION_REF'
                    # count how many and create options as self.refLogics
                    splits = ref_text.split('sonst')
                    for number, split in enumerate(splits):
                        if number == 0:
                            self.RefLogic.options.append(RefLogicOption(type = 'OPTION_WITH_CONTENT_ID', questionContentId=ref_number+1, questionId=create_id(self, split)))
                        if number > 0:
                            self.RefLogic.options.append(RefLogicOption(type = 'OPTION_WITH_CONTENT_ID_SKIP', questionContentId=ref_number+1, questionId=create_id(self, split)))
                    # set text to '' else it will appear in worldobjectentry
                    self.texts[ref_number] = 'null'
        
       
    def fill_in_parameters(self):
        for number, option in enumerate(self.options):
            option.id = self.id + '-refopt' + str(number+1)
            option.order = number+1
            option.questionContentId = self.id + "-" + str(option.questionContentId)
            option.questionRefLogicId = self.id

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

    