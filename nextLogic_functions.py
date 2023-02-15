
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

def create_nextLogic_options(id_base, answer_option_base, next_logics):
    if next_logics == None:
        return ""
    count = 0
    next_logics_block = '' 
    for number, letter in enumerate(next_logics):
        if letter == 'N':
            if number != 0:
                next_logics_block += ","
            next_logics_block += create_next_logic_option(id_base, count, answer_option_base)
        count+=1
    return next_logics_block
