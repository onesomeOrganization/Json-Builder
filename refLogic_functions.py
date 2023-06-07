
def create_refLogic_options(question):
    refLogic_options = ''
    for num, refLogic_id in enumerate(question.refLogic_options['OPTION']):
        refLogic_options += '''
                {
                  "id": "%s-%s",
                  "order": %s,
                  "type": "OPTION",
                  "number": null,
                  "questionRefLogicId": "%s",
                  "questionAnswerOptionId": null,
                  "secondQuestionAnswerOptionId": null,
                  "questionContentId": null,
                  "questionId": "%s",
                  "questionContentSubContentId": null,
                  "limit": null
                },''' %(question.id_base+question.version+'-'+question.etappe+'-'+question.screen, num+1, num+1, question.id_base+question.version+'-'+question.etappe+'-'+question.screen, refLogic_id)
        if num == len(question.refLogic_options['OPTION'])-1:
            refLogic_options = refLogic_options[:-1]
    return refLogic_options

def create_refLogic(question):
    if question.refLogic_type == None:
        return ''
    refLogic = '''"refLogic": {
              "id": "%s",
              "type": "%s",
              "refQuestionId": null,
              "options": [%s
              ]
            },''' %(question.id_base+question.version+'-'+question.etappe+'-'+question.screen, question.refLogic_type, create_refLogic_options(question))
    return refLogic