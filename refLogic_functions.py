class RefLogic:
    def __init__(self, id = 'XY', type = 'XY', refQuestionId = 'XY', options = []):
        self.type = type
        self.id = id
        self.refQuestionId = refQuestionId
        self.options = options
        self.json = ''
       
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

    