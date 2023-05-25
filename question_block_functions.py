from content_block_functions import create_content_block
from answer_option_functions import *
from nextLogic_functions import *

def create_beginning(id, version, journey_key, information):
    beginning = '''
{
  "id": "%s",
  "key": "%s",
  "order": 10,
  "mainImageName": "%s",
  "mainImageLongName": "%s",
  "topicIconImageName": "%s",
  "mainImageLockedLongName": "%s",
  "backgroundImageName": "%s",
  "sessionImageName": "%s",
  "published": true,
  "publishedEN": false,
  "feedbackLink": null,
  "version": %s,
  "type": "%s",
  "compulsoryOrder": false,
  "topicId": %s,
  "backgroundImageLockedName": "dark_main.png",
  "translations": [
    {
      "id": "%s-DE",
      "language": "DE",
      "title": "%s",
      "subTitle": "",
      "description": null
    },
    {
      "id": "%s-EN",
      "language": "EN",
      "title": "Englisch",
      "subTitle": "",
      "description": null
    }
  ],
  "content": [
    {
      "id": "%s-cont",
      "order": 2,
      "type": "PARAGRAPH",
      "imageName": null,
      "translations": [
        {
          "id": "%s-cont-DE",
          "language": "DE",
          "title": null,
          "text": "%s"
        },
        {
          "id": "%s-cont-EN",
          "language": "EN",
          "title": null,
          "text": "Englisch"
        }
      ]
    },
    {
      "id": "%s-s1",
      "order": 4,
      "type": "SESSION_TITLE",
      "imageName": null,
      "translations": [
        {
          "id": "%s-s1-DE",
          "language": "DE",
          "title": null,
          "text": "%s"
        },
        {
          "id": "%s-s1-EN",
          "language": "EN",
          "title": null,
          "text": "Englisch"
        }
      ]
    }
  ],
  "sessions": [
    {
      "id": "%s-1",
      "order": 1,
      "durationMin": %s,
      "durationMax": %s,
      "translations": [
        {
          "id": "%s-1-DE",
          "language": "DE",
          "title": "%s"
        },
        {
          "id": "%s-1-EN",
          "language": "EN",
          "title": "Englisch"
        }
      ],
      "questions": [
        ''' % (id+version, journey_key, information[9], information[10], information[11], information[12], information[13], information[14], version, information[0], information[1], id+version, information[2], id+version, id+version, id+version, information[3].replace('"', '\\"').replace('\n', '').replace("_x000B_", "")+'<br><br>', id+version, id+version, id+version, information[4], id+version, id+version, information[7], information[8], id+version, information[5], id+version)
    return beginning

def get_content_length(structure):
    length = 0
    for entry in structure:
      if entry == 'REFERENCE':
        length+=1
      elif entry == 'PARAGRAPH':
        length+=1
      elif entry == 'AUDIO':
        length+=2
      elif entry == 'IMAGE':
        length+=2
      elif entry == 'MORE_INFORMATION_EXPANDED':
        length+=1
      elif entry == 'MORE_INFORMATION':
        length+=1
    return length

def create_question(question, id_base, count, write_beginning, id_base_next_question, question_id, version, etappe):
    content_length = get_content_length(question.structure)+2 # fragen fangen nicht von 0 an und Subititel 
    type = question.type
    answer_options = question.answer_option
    next_logics = question.next_logic_option
    next_logic_type = question.next_logic_type
    texts = question.texts

    # DICTIONARY
    return {
        "CONTENT": ''' 
        {
          "id": "%s",
          "type": "CONTENT",
          "number": null,
          "minNumber": null,
          "maxNumber": null,
          "screenDuration": null,
          "reviewAble": %s,
          "noAnswerPreselection": null,
          "showHint": null,
          "progress": %s,
          "worldObjectEntryKeyType": %s,
          "nonOptionalKeyInsightHint": false,
          "optional": %s,
          "firstJourneyQuestion": %s,
          "firstSessionQuestion": %s,
          "questionLoopId": null,
          "translations": [],
          "content": [
            {
              "id": "%s-1",
              "type": "SUB_TITLE",
              "required": null,
              "showHidden": null,
              "order": 1,
              "imageName": null,
              "audioName": null,
              "style": null,
              "refAdaptionType": null,
              "refAdaptionNumber": null,
              "refOrderType": null,
              "refOrderColumn": null,
              "refOffset": null,
              "refLimit": null,
              "downloadName": null,
              "checkForSpecialTextReplacement": null,
              "questionAnswerOptionId": null,
              "language": null,
              "contentShowType": null,
              "worldObjectEntryKey": null,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [
                {
                  "id": "%s-1-DE",
                  "language": "DE",
                  "title": null,
                  "text": "%s"
                },
                {
                  "id": "%s-1-EN",
                  "language": "EN",
                  "title": null,
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            }%s
          ],
          "nextLogic": {
            "id": "%s",
            "type": "%s",
            "count": null,
            "nextQuestionId": %s,
            "prevQuestionId": null,
            "refQuestionId": null,
            "questionRefLogicId": null,
            "sessionId": null,
            "options": [
            %s
            ],
            "refAdaptions": []
          }
        },''' % (question_id, question.reviewable, question.progress, question.worldObjectEntryKeyType, question.optional, "true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", question_id, question_id, texts[0], question_id, create_content_block(question_id, 2, question.structure, texts), question_id, next_logic_type, id_base_next_question, create_nextLogic_options(question_id, content_length, next_logics, next_logic_type, question.reference_of_next_question, id_base_next_question, question.next_logic_option_screen_refs)),
        "OPTION_QUESTION": '''
        {
          "id": "%s",
          "type": "OPTION_QUESTION",
          "number": null,
          "minNumber": null,
          "maxNumber": null,
          "screenDuration": null,
          "reviewAble": %s,
          "noAnswerPreselection": null,
          "showHint": null,
          "progress": %s,
          "worldObjectEntryKeyType": %s,
          "nonOptionalKeyInsightHint": false,
          "optional": %s,
          "firstJourneyQuestion": %s,
          "firstSessionQuestion": %s,
          "questionLoopId": null,
          "translations": [],
          "content": [
            {
              "id": "%s-1",
              "type": "SUB_TITLE",
              "required": null,
              "showHidden": null,
              "order": 1,
              "imageName": null,
              "audioName": null,
              "style": null,
              "refAdaptionType": null,
              "refAdaptionNumber": null,
              "refOrderType": null,
              "refOrderColumn": null,
              "refOffset": null,
              "refLimit": null,
              "downloadName": null,
              "checkForSpecialTextReplacement": null,
              "questionAnswerOptionId": null,
              "language": null,
              "contentShowType": null,
              "worldObjectEntryKey": null,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [
                {
                  "id": "%s-1-DE",
                  "language": "DE",
                  "title": null,
                  "text": "%s"
                },
                {
                  "id": "%s-1-EN",
                  "language": "EN",
                  "title": "",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            }%s
            ,{
              "id": "%s-%s",
              "type": "ANSWER_OPTION",
              "required": true,
              "showHidden": null,
              "order": %s,
              "imageName": null,
              "audioName": null,
              "style": null,
              "refAdaptionType": null,
              "refAdaptionNumber": null,
              "refOrderType": null,
              "refOrderColumn": null,
              "refOffset": null,
              "refLimit": null,
              "downloadName": null,
              "checkForSpecialTextReplacement": null,
              "questionAnswerOptionId": null,
              "language": null,
              "contentShowType": null,
              "worldObjectEntryKey": null,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [],
              "answerOptions": [
                {
                  "id": "%s-%s-1",
                  "order": 1,
                  "number": null,
                  "type": "BUTTON",
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
                      "id": "%s-%s-1-DE",
                      "language": "DE",
                      "title": null,
                      "text": "%s",
                      "description": ""
                    },
                    {
                      "id": "%s-%s-1-EN",
                      "language": "EN",
                      "title": "",
                      "text": "Englisch",
                      "description": ""
                    }
                  ]
                },
                {
                  "id": "%s-%s-2",
                  "order": 2,
                  "number": null,
                  "type": "BUTTON",
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
                      "id": "%s-%s-2-DE",
                      "language": "DE",
                      "title": null,
                      "text": "%s",
                      "description": ""
                    },
                    {
                      "id": "%s-%s-2-EN",
                      "language": "EN",
                      "title": "",
                      "text": "Englisch",
                      "description": ""
                    }
                  ]
                }
              ]
            }
          ],
          "nextLogic": {
            "id": "%s",
            "type": "NEXT_OPTION",
            "count": null,
            "nextQuestionId": null,
            "prevQuestionId": null,
            "refQuestionId": null,
            "questionRefLogicId": null,
            "sessionId": null,
            "options": [
              {
                "id": "%s-opt1",
                "order": null,
                "type": "NEXT",
                "number": null,
                "count": null,
                "secondNumber": null,
                "secondCount": null,
                "questionAnswerOptionId": "%s-%s-1",
                "secondQuestionAnswerOptionId": null,
                "questionId": "%s",
                "refQuestionId": null
              },
              {
                "id": "%s-opt2",
                "order": null,
                "type": "NEXT",
                "number": null,
                "count": null,
                "secondNumber": null,
                "secondCount": null,
                "questionAnswerOptionId": "%s-%s-2",
                "secondQuestionAnswerOptionId": null,
                "questionId": "%s",
                "refQuestionId": null
              }
            ],
            "refAdaptions": []
          }
        },'''% (question_id, question.reviewable, question.progress, question.worldObjectEntryKeyType, question.optional, "true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", question_id, question_id, texts[0], question_id, create_content_block(question_id,2, question.structure, texts),question_id, content_length, content_length, question_id, content_length, question_id, content_length, question.button_one_text, question_id, content_length, question_id, content_length, question_id, content_length, question.button_two_text, question_id, content_length, question_id, question_id, question_id, content_length, question.button_one_nextquestion,  question_id, question_id, content_length, question.button_two_nextquestion),
        "OPEN_QUESTION": '''
        {
          "id": "%s",
          "type": "OPEN_QUESTION",
          "number": null,
          "minNumber": null,
          "maxNumber": null,
          "screenDuration": null,
          "reviewAble": %s,
          "noAnswerPreselection": null,
          "showHint": null,
          "progress": %s,
          "worldObjectEntryKeyType": %s,
          "nonOptionalKeyInsightHint": false,
          "optional": %s,
          "firstJourneyQuestion": %s,
          "firstSessionQuestion": %s,
          "questionLoopId": null,
          "translations": [],
          "content": [
            {
              "id": "%s-1",
              "type": "SUB_TITLE",
              "required": null,
              "showHidden": null,
              "order": 1,
              "imageName": null,
              "audioName": null,
              "style": null,
              "refAdaptionType": null,
              "refAdaptionNumber": null,
              "refOrderType": null,
              "refOrderColumn": null,
              "refOffset": null,
              "refLimit": null,
              "downloadName": null,
              "checkForSpecialTextReplacement": null,
              "questionAnswerOptionId": null,
              "language": null,
              "contentShowType": null,
              "worldObjectEntryKey": null,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [
                {
                  "id": "%s-1-DE",
                  "language": "DE",
                  "title": null,
                  "text": "%s"
                },
                {
                  "id": "%s-1-EN",
                  "language": "EN",
                  "title": "",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            }%s     
            ,{
              "id": "%s-%s",
              "type": "ANSWER_OPTION",
              "required": true,
              "showHidden": null,
              "order": %s,
              "imageName": null,
              "audioName": null,
              "style": null,
              "refAdaptionType": null,
              "refAdaptionNumber": null,
              "refOrderType": null,
              "refOrderColumn": null,
              "refOffset": null,
              "refLimit": null,
              "downloadName": null,
              "checkForSpecialTextReplacement": null,
              "questionAnswerOptionId": null,
              "language": null,
              "contentShowType": null,
              "worldObjectEntryKey": null,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [],
              "answerOptions": [
                {
                  "id": "%s-%s-1",
                  "order": 1,
                  "number": null,
                  "type": "TEXT_FIELD",
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
                }
              ]
            }
          ],
          "nextLogic": {
            "id": "%s",
            "type": "%s",
            "count": null,
            "nextQuestionId": %s,
            "prevQuestionId": null,
            "refQuestionId": null,
            "questionRefLogicId": null,
            "sessionId": null,
            "options": [
            %s
            ],
            "refAdaptions": []
          }
        },''' % (question_id, question.reviewable, question.progress, question.worldObjectEntryKeyType, question.optional, "true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", question_id,question_id,texts[0], question_id,create_content_block(question_id, 2, question.structure, texts), question_id, content_length, content_length, question_id, content_length, question_id, next_logic_type,id_base_next_question,create_nextLogic_options(question_id, content_length, next_logics, next_logic_type, question.reference_of_next_question, id_base_next_question, question.next_logic_option_screen_refs)),
        "SCALA_SLIDER":'''
        {
          "id": "%s",
          "type": "SCALA_SLIDER",
          "number": null,
          "minNumber": %s,
          "maxNumber": %s,
          "screenDuration": null,
          "reviewAble": %s,
          "noAnswerPreselection": null,
          "showHint": null,
          "progress": %s,
          "worldObjectEntryKeyType": %s,
          "nonOptionalKeyInsightHint": false,
          "optional": %s,
          "firstJourneyQuestion": %s,
          "firstSessionQuestion": %s,
          "questionLoopId": null,
          "translations": [],
          "content": [
            {
              "id": "%s-1",
              "type": "SUB_TITLE",
              "required": null,
              "showHidden": null,
              "order": 1,
              "imageName": null,
              "audioName": null,
              "style": null,
              "refAdaptionType": null,
              "refAdaptionNumber": null,
              "refOrderType": null,
              "refOrderColumn": null,
              "refOffset": null,
              "refLimit": null,
              "downloadName": null,
              "checkForSpecialTextReplacement": null,
              "questionAnswerOptionId": null,
              "language": null,
              "contentShowType": null,
              "worldObjectEntryKey": null,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [
                {
                  "id": "%s-1-DE",
                  "language": "DE",
                  "title": null,
                  "text": "%s"
                },
                {
                  "id": "%s-1-EN",
                  "language": "EN",
                  "title": null,
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            }%s
            ,{
              "id": "%s-%s",
              "type": "ANSWER_OPTION",
              "required": true,
              "showHidden": null,
              "order": %s,
              "imageName": null,
              "audioName": null,
              "style": null,
              "refAdaptionType": null,
              "refAdaptionNumber": null,
              "refOrderType": null,
              "refOrderColumn": null,
              "refOffset": null,
              "refLimit": null,
              "downloadName": null,
              "checkForSpecialTextReplacement": null,
              "questionAnswerOptionId": null,
              "language": null,
              "contentShowType": null,
              "worldObjectEntryKey": null,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [],
              "answerOptions": [
                {
                  "id": "%s-%s-1",
                  "order": 1,
                  "number": null,
                  "type": "SLIDER",
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
                      "id": "%s-%s-1-DE",
                      "language": "DE",
                      "title": null,
                      "text": "%s, ,%s",
                      "description": ""
                    },
                    {
                      "id": "%s-%s-1-EN",
                      "language": "EN",
                      "title": null,
                      "text": "Englisch",
                      "description": ""
                    }
                  ]
                }
              ]
            }
          ],
          "nextLogic": {
            "id": "%s",
            "type": "%s",
            "count": null,
            "nextQuestionId": %s,
            "prevQuestionId": null,
            "refQuestionId": null,
            "questionRefLogicId": null,
            "sessionId": null,
            "options": [
            %s
            ],
            "refAdaptions": []
          }
        },''' % (question_id,question.scala_min,question.scala_max, question.reviewable, question.progress, question.worldObjectEntryKeyType, question.optional, "true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", question_id, question_id,texts[0], question_id, create_content_block(question_id, 2, question.structure, texts) ,question_id, content_length, content_length, question_id, content_length, question_id, content_length, question.scala_min_text, question.scala_max_text,question_id, content_length, question_id, next_logic_type,id_base_next_question,create_nextLogic_options(question_id, content_length, next_logics, next_logic_type, question.reference_of_next_question, id_base_next_question, question.next_logic_option_screen_refs)),
        "ITEM_LIST_EXPANDABLE": '''
        {
          "id": "%s",
          "type": "ITEM_LIST_EXPANDABLE",
          "number": null,
          "minNumber": 1,
          "maxNumber": %s,
          "screenDuration": null,
          "reviewAble": %s,
          "noAnswerPreselection": null,
          "showHint": null,
          "progress": %s,
          "worldObjectEntryKeyType": %s,
          "nonOptionalKeyInsightHint": false,
          "optional": %s,
          "firstJourneyQuestion": %s,
          "firstSessionQuestion": %s,
          "questionLoopId": null,
          "translations": [],
          "content": [
            {
              "id": "%s-1",
              "type": "SUB_TITLE",
              "required": null,
              "showHidden": null,
              "order": 1,
              "imageName": null,
              "audioName": null,
              "style": null,
              "refAdaptionType": null,
              "refAdaptionNumber": null,
              "refOrderType": null,
              "refOrderColumn": null,
              "refOffset": null,
              "refLimit": null,
              "downloadName": null,
              "checkForSpecialTextReplacement": null,
              "questionAnswerOptionId": null,
              "language": null,
              "contentShowType": null,
              "worldObjectEntryKey": null,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [
                {
                  "id": "%s-1-DE",
                  "language": "DE",
                  "title": null,
                  "text": "%s"
                },
                {
                  "id": "%s-1-EN",
                  "language": "EN",
                  "title": "",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            }%s
            ,{
              "id": "%s-%s",
              "type": "ANSWER_OPTION",
              "required": %s,
              "showHidden": null,
              "order": %s,
              "imageName": null,
              "audioName": null,
              "style": null,
              "refAdaptionType": null,
              "refAdaptionNumber": null,
              "refOrderType": null,
              "refOrderColumn": null,
              "refOffset": null,
              "refLimit": null,
              "downloadName": null,
              "checkForSpecialTextReplacement": null,
              "questionAnswerOptionId": null,
              "language": null,
              "contentShowType": null,
              "worldObjectEntryKey": null,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [],
              "answerOptions": [
                %s
              ]
            }
          ],
          "nextLogic": {
            "id": "%s",
            "type": "%s",
            "count": null,
            "nextQuestionId": %s,
            "prevQuestionId": null,
            "refQuestionId": null,
            "questionRefLogicId": null,
            "sessionId": null,
            "options": [
              %s
            ],
            "refAdaptions": []
          }
        },''' % (question_id, question.maxNumber, question.reviewable, question.progress, question.worldObjectEntryKeyType, question.optional, "true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", question_id,question_id, texts[0], question_id,create_content_block(question_id, 2, question.structure, texts), question_id, content_length, question.answer_required, content_length, create_answer_options(question, question_id, content_length,answer_options, texts), question_id, next_logic_type, id_base_next_question, create_nextLogic_options(question_id, content_length, next_logics, next_logic_type, question.reference_of_next_question, id_base_next_question, question.next_logic_option_screen_refs)),
        "ITEM_LIST_SINGLE_CHOICE": '''
        {
          "id": "%s",
          "type": "ITEM_LIST_SINGLE_CHOICE",
          "number": null,
          "minNumber": null,
          "maxNumber": null,
          "screenDuration": null,
          "reviewAble": %s,
          "noAnswerPreselection": null,
          "showHint": null,
          "progress": %s,
          "worldObjectEntryKeyType": %s,
          "nonOptionalKeyInsightHint": false,
          "optional": %s,
          "firstJourneyQuestion": %s,
          "firstSessionQuestion": %s,
          "questionLoopId": null,
          "translations": [],
          "content": [
            {
              "id": "%s-1",
              "type": "SUB_TITLE",
              "required": null,
              "showHidden": null,
              "order": 1,
              "imageName": null,
              "audioName": null,
              "style": null,
              "refAdaptionType": null,
              "refAdaptionNumber": null,
              "refOrderType": null,
              "refOrderColumn": null,
              "refOffset": null,
              "refLimit": null,
              "downloadName": null,
              "checkForSpecialTextReplacement": null,
              "questionAnswerOptionId": null,
              "language": null,
              "contentShowType": null,
              "worldObjectEntryKey": null,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [
                {
                  "id": "%s-1-DE",
                  "language": "DE",
                  "title": null,
                  "text": "%s"
                },
                {
                  "id": "%s-1-EN",
                  "language": "EN",
                  "title": null,
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            }%s
            ,{
              "id": "%s-%s",
              "type": "ANSWER_OPTION",
              "required": true,
              "showHidden": null,
              "order": %s,
              "imageName": null,
              "audioName": null,
              "style": null,
              "refAdaptionType": null,
              "refAdaptionNumber": null,
              "refOrderType": null,
              "refOrderColumn": null,
              "refOffset": null,
              "refLimit": null,
              "checkForSpecialTextReplacement": null,
              "questionAnswerOptionId": null,
              "language": null,
              "refQuestionId": null,
              "translations": [],
              "answerOptions": [
                %s
              ]
            }
          ],
          "nextLogic": {
            "id": "%s",
            "type": "%s",
            "count": null,
            "nextQuestionId": %s,
            "prevQuestionId": null,
            "refQuestionId": null,
            "questionRefLogicId": null,
            "sessionId": null,
            "options": [
              %s
            ],
            "refAdaptions": []
          }
        },'''%(question_id, question.reviewable, question.progress, question.worldObjectEntryKeyType, question.optional,"true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", question_id, question_id,texts[0], question_id, create_content_block(question_id,2, question.structure, texts), question_id, content_length, content_length, create_answer_options(question, question_id, content_length,answer_options, texts), question_id, next_logic_type,id_base_next_question, create_nextLogic_options(question_id, content_length, next_logics, next_logic_type, question.reference_of_next_question, id_base_next_question, question.next_logic_option_screen_refs)),
        "Neue Etappe": '''
        ],
      "questionLoops": []
    },
    {
      "id": "%s%s-%s",
      "order": %s,
      "durationMin": %s,
      "durationMax": %s,
      "translations": [
        {
          "id": "%s%s-%s-DE",
          "language": "DE",
          "title": "%s"
        },
        {
          "id": "%s%s-%s-EN",
          "language": "EN",
          "title": "Englisch"
        }
      ],
      "questions": [
        '''%(id_base, version, etappe, etappe, int(texts[np.where(question.structure == 'Zeit min')][0]) if 'Zeit min' in question.structure else '', int(texts[np.where(question.structure == 'Zeit max')][0]) if 'Zeit max' in question.structure else '', id_base, version, etappe, texts[np.where(question.structure == 'Etappen-Titel')][0] if 'Zeit min' in question.structure else '',id_base, version, etappe)
        }.get(type, None) 
    