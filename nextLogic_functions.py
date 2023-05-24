
def create_next_logic_option(id_base, count, answer_option_base, next_logic_option_screen_ref):
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
                "questionId": "%s",
                "refQuestionId": null
              }''' %(id_base, count, id_base, answer_option_base, count, next_logic_option_screen_ref)
    return next_logic_option

def create_ref_key_insight_option(id_base, reference_of_next_question, id_base_next_question, id_base_skip_question):
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
              }''' %(id_base, id_base_next_question, id_base, id_base_skip_question ,id_base, id_base_next_question, reference_of_next_question)
    return ref_key_insight_option

def create_nextLogic_options(id_base, answer_option_base, next_logics, next_logic_type, reference_of_next_question, id_base_next_question, next_logic_option_screen_refs):
    next_logics_block = '' 
    # for key insights
    if next_logic_type == 'REF_KEY_INSIGHT':
        plus_one = int(id_base_next_question[-2])+1
        id_base_skip_question = id_base_next_question[:-2] + str(plus_one) + '"'
        next_logics_block += create_ref_key_insight_option(id_base, reference_of_next_question, id_base_next_question, id_base_skip_question)
    count = 1
    # if no logics just return empty
    if len(next_logics) == 0:
        return next_logics_block
    for number, letter in enumerate(next_logics):
        if letter == 'N':
            if number != 0:
                next_logics_block += ","
            next_logics_block += create_next_logic_option(id_base, count, answer_option_base, next_logic_option_screen_refs[number])
        count+=1
    return next_logics_block
