
def create_next_logic_option(id_base, count, answer_option_base):
    next_logic_option = '''
                {
                "id": "%s-opt%s",
                "order": null,
                "type": "NEXT",
                "number": null,
                "count": null,
                "secondNumber": null,
                "secondCount": null,
                "questionAnswerOptionId": "%s-%s-%s",
                "secondQuestionAnswerOptionId": null,
                "questionId": "XY",
                "refQuestionId": null
              }''' %(id_base, count, id_base, answer_option_base, count)
    return next_logic_option

def create_ref_key_insight_option(id_base):
    ref_key_insight_option = '''
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
                "questionId": "XY-ifkeyexists",
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
                "questionId": "XY-ifkeynotexists",
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
                "questionId": "XY-ifkeyexists",
                "worldObjectEntryKey": "XY-KEY",
                "refQuestionId": null
              }''' %(id_base, id_base, id_base)
    return ref_key_insight_option

def create_nextLogic_options(id_base, answer_option_base, next_logics, next_logic_type):
    next_logics_block = '' 
    if next_logic_type == 'REF_KEY_INSIGHT':
        next_logics_block += create_ref_key_insight_option(id_base)
    if next_logics == None:
        return next_logics_block
    count = 1
    for number, letter in enumerate(next_logics):
        if letter == 'N':
            if number != 0:
                next_logics_block += ","
            next_logics_block += create_next_logic_option(id_base, count, answer_option_base)
        count+=1
    return next_logics_block
