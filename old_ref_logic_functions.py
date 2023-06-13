def create_refLogic_options(option):
    refLogic_option = '''
                {
                  "id": "%s",
                  "order": %s,
                  "type": "%s",
                  "number": null,
                  "questionRefLogicId": "%s",
                  "questionAnswerOptionId": null,
                  "secondQuestionAnswerOptionId": null,
                  "questionContentId": null,
                  "questionId": "%s",
                  "questionContentSubContentId": null,
                  "limit": null
                },''' %(option.id, option.order, option.type,  option.questionRefLogicId, option.questionContentId, option.questionId)
    return refLogic_option

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
                },''' %(question.id_base+question.version+'-'+question.etappe+'-'+question.screen+'-refopt', num+1, num+1, question.id_base+question.version+'-'+question.etappe+'-'+question.screen, refLogic_id)
        if num == len(question.refLogic_options['OPTION'])-1:
            refLogic_options = refLogic_options[:-1]
    return refLogic_options

def creat_refLogic_options_with_contentID(question):
    refLogic_options_with_contentID = ''
    for num, refLogic_id in enumerate(question.refLogic_options['OPTION_WITH_CONTENT_ID']):
        refLogic_options_with_contentID += '''
                {
                  "id": "%s-%s",
                  "order": %s,
                  "type": "OPTION_WITH_CONTENT_ID",
                  "number": null,
                  "questionRefLogicId": "%s",
                  "questionAnswerOptionId": null,
                  "secondQuestionAnswerOptionId": null,
                  "questionContentId": null,
                  "questionId": "%s",
                  "questionContentSubContentId": null,
                  "limit": null
                },''' %(question.id_base+question.version+'-'+question.etappe+'-'+question.screen+'-refopt', num+1, num+1, question.id_base+question.version+'-'+question.etappe+'-'+question.screen, refLogic_id)
        if num == len(question.refLogic_options_with_contentID['OPTION_WITH_CONTENT_ID'])-1:
            refLogic_options_with_contentID = refLogic_options_with_contentID[:-1]
    return refLogic_options_with_contentID

def create_refLogic(question):
    for option in question.RefLogic.options:
        ref_options = create_refLogic_options(option)
        # TODO: komma weg beim letzten



    if question.refLogic_type == None:
        return ''
    if 'OPTION' in question.refLogic_options:
        for option in question.refLogic_options['OPTION']:
            ref_options = create_refLogic_options(option)
            
    elif 'OPTION_WITH_CONTENT_ID' in question.refLogic_options:
        ref_options = creat_refLogic_options_with_contentID(question)
    refLogic = '''"refLogic": {
              "id": "%s",
              "type": "%s",
              "refQuestionId": null,
              "options": [%s
              ]
            },''' %(question.id_base+question.version+'-'+question.etappe+'-'+question.screen, question.refLogic_type, ref_options)
    return refLogic