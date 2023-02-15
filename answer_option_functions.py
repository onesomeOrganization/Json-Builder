def create_radiobutton(id_base, answer_option_base, count):
    radiobutton = '''
                {
                  "id": "%s-%s-%s",
                  "order": %s,
                  "number": null,
                  "type": "RADIO_BUTTON",
                  "imageName": null,
                  "hidden": null,
                  "escapeOption": null,
                  "sliderType": null,
                  "negative": null,
                  "unselectOthers": null,
                  "refQuestionAnswerOptionId": null,
                  "questionLoopCycleId": null,
                  "translations": [
                    {
                      "id": "%s-%s-%s-DE",
                      "language": "DE",
                      "title": null,
                      "text": "XY",
                      "description": ""
                    },
                    {
                      "id": "%s-%s-%s-EN",
                      "language": "EN",
                      "title": null,
                      "text": "Englisch",
                      "description": ""
                    }
                  ]
                }'''%(id_base, answer_option_base ,count, count, id_base, answer_option_base, count, id_base, answer_option_base, count)
    return radiobutton

def create_checkbox(id_base, answer_option_base, count):
  checkbox = '''
                {
                  "id": "%s-%s-%s",
                  "order": %s,
                  "number": null,
                  "type": "CHECKBOX",
                  "imageName": null,
                  "hidden": null,
                  "escapeOption": null,
                  "sliderType": null,
                  "negative": null,
                  "unselectOthers": null,
                  "booleanHelper": null,
                  "refQuestionAnswerOptionId": null,
                  "secondRefQuestionAnswerOptionId": null,
                  "questionLoopCycleId": null,
                  "translations": [
                    {
                      "id": "%s-%s-%s-DE",
                      "language": "DE",
                      "title": null,
                      "text": "XY",
                      "description": ""
                    },
                    {
                      "id": "%s-%s-%s-EN",
                      "language": "EN",
                      "title": "",
                      "text": "Englisch",
                      "description": ""
                    }
                  ]
                }'''%(id_base, answer_option_base ,count, count, id_base, answer_option_base, count, id_base, answer_option_base, count)
  return checkbox

def create_text_field_expandable(id_base, answer_option_base, count):
  text_field_expandable = '''
                {
                  "id": "%s-%s-%s",
                  "order": %s,
                  "number": null,
                  "type": "TEXT_FIELD_EXPANDABLE",
                  "imageName": null,
                  "hidden": null,
                  "escapeOption": null,
                  "sliderType": null,
                  "negative": null,
                  "unselectOthers": null,
                  "booleanHelper": null,
                  "refQuestionAnswerOptionId": null,
                  "secondRefQuestionAnswerOptionId": null,
                  "questionLoopCycleId": null,
                  "translations": []
                }'''%(id_base, answer_option_base ,count, count)
  return text_field_expandable

def create_answer_options(id_base, answer_option_base, answer_options, question):
    if answer_options == None:
        return ""
    count = 1
    answer_options_block = '' 
    for number, letter in enumerate(answer_options):
        if letter == 'R':
            if number != 0:
                answer_options_block += ","
            answer_options_block += create_radiobutton(id_base, answer_option_base, count)
            count+=1
        if letter == 'C':
            if number != 0:
                answer_options_block += ","
            answer_options_block += create_checkbox(id_base, answer_option_base, count)
            count+=1
        if letter == 'T':
            if number != 0:
                answer_options_block += ","
            answer_options_block += create_text_field_expandable(id_base, answer_option_base, count)
            count+=1
    return answer_options_block