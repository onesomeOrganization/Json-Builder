import os
import sys
# 
#  ------ VARIABLES ------------------------------------
# Auszufüllen
name_of_json_file = "Kreativitätsboost_weitere-Screens"
journey_key = "Test_Short_Trip_Flora"
id = "flora-v"
version = str(5)
write_beginning = False
write_ending = False
# CONTENT -> SP, OPTION_QUESTION ->SPA, OPEN_QUESTION ->SPA, OPEN_QUESTION_REF ->SPRPA, SCALA_SLIDER, ITEM_LIST_EXPANDABLE, AUDIO
# + multiple PRPR... works only for CONTENT so far
# or A for Audio & I for Image
questions_array  = ["OPEN_QUESTION_REF", "OPEN_QUESTION", "OPEN_QUESTION_REF", "CONTENT", "CONTENT+RPRPRPR", "OPEN_QUESTION", "CONTENT"] 
etappe = "-1-"
startnumber = 16

# ------- HELPER FUNCTIONS ------------------------------

def create_ref(id_base, count):
  referenzierung = '''  
            ,{
              "id": "%s-%s",
              "type": "ANSWER_OPTION_REF",
              "required": null,
              "showHidden": null,
              "order": %s,
              "imageName": null,
              "audioName": null,
              "style": "TEXT",
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
              "refQuestionId": "XY",
              "refQuestionAnswerOptionId": null,
              "translations": [],
              "answerOptions": []
            }'''%(id_base, count, count)
  return referenzierung

def create_par(id_base, count):
  paragraph = '''
            ,{
              "id": "%s-%s",
              "type": "PARAGRAPH",
              "required": null,
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
              "translations": [
                {
                  "id": "%s-%s-DE",
                  "language": "DE",
                  "title": null,
                  "text": "XY"
                },
                {
                  "id": "%s-%s-EN",
                  "language": "EN",
                  "title": null,
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            }'''%(id_base, count, count, id_base, count, id_base, count)
  return paragraph

def create_audio(id_base, count):
  audio = '''
            ,{
              "id": "%s-%s",
              "type": "AUDIO",
              "required": null,
              "showHidden": null,
              "order": %s,
              "imageName": null,
              "audioName": "XY",
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
              "language": "DE",
              "contentShowType": null,
              "worldObjectEntryKey": null,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [],
              "answerOptions": []
            },
            {
              "id": "%s-%s",
              "type": "AUDIO",
              "required": null,
              "showHidden": null,
              "order": %s,
              "imageName": null,
              "audioName": "XY",
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
              "language": "EN",
              "contentShowType": null,
              "worldObjectEntryKey": null,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [],
              "answerOptions": []
            }'''%(id_base, count, count, id_base, count, count)
  return audio

def create_image(id_base, count):
  image = '''
            ,{
              "id": "%s-%s",
              "type": "IMAGE",
              "required": null,
              "showHidden": null,
              "order": %s,
              "imageName": "XY",
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
              "language": "DE",
              "contentShowType": null,
              "worldObjectEntryKey": null,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [],
              "answerOptions": []
            },
            {
              "id": "%s-%s",
              "type": "IMAGE",
              "required": null,
              "showHidden": null,
              "order": %s,
              "imageName": "XY",
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
              "language": "EN",
              "contentShowType": null,
              "worldObjectEntryKey": null,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [],
              "answerOptions": []
            }'''%(id_base, count, count, id_base, count, count)
  return image

def create_ref_block(id_base, count, refs):
  ref_block = '' 
  for letter in refs:
    if letter == 'R':
      ref_block += create_ref(id_base, count)
    elif letter == 'P':
      ref_block += create_par(id_base, count)
    elif letter == 'A':
      ref_block += create_audio(id_base, count)
    elif letter == 'I':
      ref_block += create_image(id_base, count)
    count+=1

  return ref_block



# -------- WRITE FILE -------------------------------------



with open(os.path.join(sys.path[0], name_of_json_file+".json"), 'w+') as file:

# BEGINNING
    if write_beginning:    
        file.write('''
{
  "id": "%s",
  "key": "%s",
  "order": 10,
  "mainImageName": "red_main.png",
  "mainImageLongName": "red_main.png",
  "topicIconImageName": "core.svg",
  "mainImageLockedLongName": "red_main.png",
  "backgroundImageName": "red_background.jpeg",
  "sessionImageName": "red_session.png",
  "published": true,
  "publishedEN": false,
  "feedbackLink": null,
  "version": %s,
  "type": "SHORT_TRIP",
  "compulsoryOrder": false,
  "topicId": null,
  "backgroundImageLockedName": "dark_main.png",
  "translations": [
    {
      "id": "%s-DE",
      "language": "DE",
      "title": "XY",
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
      "id": "%s-2",
      "order": 2,
      "type": "PARAGRAPH",
      "imageName": null,
      "translations": [
        {
          "id": "%s-2-DE",
          "language": "DE",
          "title": null,
          "text": "<strong>Warum?</strong> Vielleicht ist dir das auch schonmal passiert: Du hast dir vorgenommen, etwas zu verändern, aber es nie durchgezogen. Deine Veränderungsenergie war vielleicht nicht groß genug. Wenn du mit geschärftem Blick auf die einzelnen Faktoren einer Veränderung schaust, wirst du dein Vorhaben diesmal durchziehen. <br><br> <strong>Dein Ziel:</strong> Prüfe für ein bestimmtes Veränderungsvorhaben wie groß deine Veränderungsenergie ist. Hast du Lust es tatsächlich anzugehen? Oder wie kannst du die Lust vergrößern?<br><br> "
        },
        {
          "id": "%s-2-EN",
          "language": "EN",
          "title": null,
          "text": "Englisch"
        }
      ]
    },
    {
      "id": "%s-3",
      "order": 4,
      "type": "SESSION_TITLE",
      "imageName": null,
      "translations": [
        {
          "id": "%s-3-DE",
          "language": "DE",
          "title": null,
          "text": "Beginne deine Expedition"
        },
        {
          "id": "%s-3-EN",
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
      "durationMin": 10,
      "durationMax": 15,
      "translations": [
        {
          "id": "%s-1-DE",
          "language": "DE",
          "title": "Wie groß ist deine Veränderungsenergie?"
        },
        {
          "id": "%s-1-EN",
          "language": "EN",
          "title": "Englisch"
        }
      ],
      "questions": [
        ''' % (id+version, journey_key, version, id+version, id+version, id+version, id+version, id+version, id+version, id+version, id+version, id+version, id+version, id+version)
        )
# MIDDLE
    for count, question_long in enumerate(questions_array):
      if not startnumber == 0:
        id_base = id+version+etappe+str(startnumber+count)
      else:
        id_base = id+version+etappe+str(count)

      # split into question and ref
      if "+" not in question_long:
        question_long = question_long + "+"

      question_split = question_long.split("+")
      question = question_split[0]
      refs = question_split[1]


      # DICTIONARY
      questions_dict = {
        "CONTENT": ''' 
        {
          "id": "%s",
          "type": "CONTENT",
          "number": null,
          "minNumber": null,
          "maxNumber": null,
          "screenDuration": null,
          "reviewAble": null,
          "noAnswerPreselection": null,
          "showHint": null,
          "progress": 0,
          "worldObjectEntryKeyType": null,
          "nonOptionalKeyInsightHint": false,
          "optional": true,
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
                  "text": "XY"
                },
                {
                  "id": "%s-1-EN",
                  "language": "EN",
                  "title": null,
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            },
            {
              "id": "%s-2",
              "type": "PARAGRAPH",
              "required": null,
              "showHidden": null,
              "order": 2,
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
                  "id": "%s-2-DE",
                  "language": "DE",
                  "title": null,
                  "text": "XY"
                },
                {
                  "id": "%s-2-EN",
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
            "type": "NEXT",
            "count": null,
            "nextQuestionId": "XY",
            "prevQuestionId": null,
            "refQuestionId": null,
            "questionRefLogicId": null,
            "sessionId": null,
            "options": [],
            "refAdaptions": []
          }
        },''' % (id_base, "true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", id_base, id_base, id_base,id_base, id_base, id_base, create_ref_block(id_base, 3, refs), id_base),
        "OPTION_QUESTION": '''
        {
          "id": "%s",
          "type": "OPTION_QUESTION",
          "number": null,
          "minNumber": null,
          "maxNumber": null,
          "screenDuration": null,
          "reviewAble": null,
          "noAnswerPreselection": null,
          "showHint": null,
          "progress": 15,
          "worldObjectEntryKeyType": null,
          "nonOptionalKeyInsightHint": false,
          "optional": true,
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
                  "text": "XY"
                },
                {
                  "id": "%s-1-EN",
                  "language": "EN",
                  "title": "",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            },
            {
              "id": "%s-2",
              "type": "PARAGRAPH",
              "required": null,
              "showHidden": null,
              "order": 2,
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
                  "id": "%s-2-DE",
                  "language": "DE",
                  "title": null,
                  "text": "XY"
                },
                {
                  "id": "%s-2-EN",
                  "language": "EN",
                  "title": "",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            },
            {
              "id": "%s-3",
              "type": "ANSWER_OPTION",
              "required": true,
              "showHidden": null,
              "order": 3,
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
                  "id": "%s-3-1",
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
                      "id": "%s-3-1-DE",
                      "language": "DE",
                      "title": null,
                      "text": "Ja",
                      "description": ""
                    },
                    {
                      "id": "%s-3-1-EN",
                      "language": "EN",
                      "title": "",
                      "text": "Englisch",
                      "description": ""
                    }
                  ]
                },
                {
                  "id": "%s-3-2",
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
                      "id": "%s-3-2-DE",
                      "language": "DE",
                      "title": null,
                      "text": "Nein",
                      "description": ""
                    },
                    {
                      "id": "%s-3-2-EN",
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
                "questionAnswerOptionId": "%s-3-1",
                "secondQuestionAnswerOptionId": null,
                "questionId": "XY",
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
                "questionAnswerOptionId": "%s-3-2",
                "secondQuestionAnswerOptionId": null,
                "questionId": "XY",
                "refQuestionId": null
              }
            ],
            "refAdaptions": []
          }
        },'''% (id_base, "true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", id_base, id_base, id_base,id_base, id_base, id_base, id_base, id_base, id_base, id_base, id_base,id_base, id_base, id_base, id_base, id_base, id_base, id_base),
        "OPEN_QUESTION": '''
        {
          "id": "%s",
          "type": "OPEN_QUESTION",
          "number": null,
          "minNumber": null,
          "maxNumber": null,
          "screenDuration": null,
          "reviewAble": true,
          "noAnswerPreselection": null,
          "showHint": null,
          "progress": 5,
          "worldObjectEntryKeyType": null,
          "nonOptionalKeyInsightHint": false,
          "optional": true,
          "firstJourneyQuestion": %s,
          "firstSessionQuestion": %s,
          "questionLoopId": null,
          "translations": [
            {
              "id": "%s-DE",
              "language": "DE",
              "title": "",
              "text": "",
              "notAnsweredText": null
            },
            {
              "id": "%s-EN",
              "language": "EN",
              "title": "",
              "text": "",
              "notAnsweredText": null
            }
          ],
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
                  "text": "XY"
                },
                {
                  "id": "%s-1-EN",
                  "language": "EN",
                  "title": "",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            },
            {
              "id": "%s-2",
              "type": "PARAGRAPH",
              "required": null,
              "showHidden": null,
              "order": 2,
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
                  "id": "%s-2-DE",
                  "language": "DE",
                  "title": null,
                  "text": "XY"
                },
                {
                  "id": "%s-2-EN",
                  "language": "EN",
                  "title": "",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            },
            {
              "id": "%s-3",
              "type": "ANSWER_OPTION",
              "required": true,
              "showHidden": null,
              "order": 3,
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
                  "id": "%s-3-1",
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
            "type": "NEXT",
            "count": null,
            "nextQuestionId": "XY",
            "prevQuestionId": null,
            "refQuestionId": null,
            "questionRefLogicId": null,
            "sessionId": null,
            "options": [],
            "refAdaptions": []
          }
        },''' % (id_base, "true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", id_base, id_base, id_base,id_base, id_base, id_base, id_base, id_base, id_base, id_base, id_base),
        "OPEN_QUESTION_REF": '''
        {
          "id": "%s",
          "type": "OPEN_QUESTION",
          "number": null,
          "minNumber": null,
          "maxNumber": null,
          "screenDuration": null,
          "reviewAble": true,
          "noAnswerPreselection": null,
          "showHint": null,
          "progress": 5,
          "worldObjectEntryKeyType": null,
          "nonOptionalKeyInsightHint": false,
          "optional": true,
          "firstJourneyQuestion": %s,
          "firstSessionQuestion": %s,
          "questionLoopId": null,
          "translations": [
            {
              "id": "%s-DE",
              "language": "DE",
              "title": "",
              "text": "",
              "notAnsweredText": null
            },
            {
              "id": "%s-EN",
              "language": "EN",
              "title": "",
              "text": "",
              "notAnsweredText": null
            }
          ],
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
                  "text": "XY"
                },
                {
                  "id": "%s-1-EN",
                  "language": "EN",
                  "title": "",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            },
            {
              "id": "%s-2",
              "type": "PARAGRAPH",
              "required": null,
              "showHidden": null,
              "order": 2,
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
                  "id": "%s-2-DE",
                  "language": "DE",
                  "title": null,
                  "text": "XY"
                },
                {
                  "id": "%s-2-EN",
                  "language": "EN",
                  "title": "",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            },
            {
              "id": "%s-3",
              "type": "ANSWER_OPTION_REF",
              "required": null,
              "showHidden": null,
              "order": 3,
              "imageName": null,
              "audioName": null,
              "style": "TEXT",
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
              "refQuestionId": "XY",
              "refQuestionAnswerOptionId": null,
              "translations": [],
              "answerOptions": []
            },
            {
              "id": "%s-4",
              "type": "PARAGRAPH",
              "required": null,
              "showHidden": null,
              "order": 4,
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
                  "id": "%s-4-DE",
                  "language": "DE",
                  "title": null,
                  "text": "XY"
                },
                {
                  "id": "%s-4-EN",
                  "language": "EN",
                  "title": "",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            },
            {
              "id": "%s-5",
              "type": "ANSWER_OPTION",
              "required": true,
              "showHidden": null,
              "order": 5,
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
                  "id": "%s-5-1",
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
            "type": "NEXT",
            "count": null,
            "nextQuestionId": "XY",
            "prevQuestionId": null,
            "refQuestionId": null,
            "questionRefLogicId": null,
            "sessionId": null,
            "options": [],
            "refAdaptions": []
          }
        },''' % (id_base, "true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", id_base, id_base, id_base,id_base, id_base, id_base, id_base, id_base, id_base, id_base, id_base, id_base, id_base, id_base, id_base),
        "SCALA_SLIDER":'''
        {
          "id": "%s",
          "type": "SCALA_SLIDER",
          "number": null,
          "minNumber": 0,
          "maxNumber": 10,
          "screenDuration": null,
          "reviewAble": null,
          "noAnswerPreselection": null,
          "showHint": null,
          "progress": 4,
          "worldObjectEntryKeyType": null,
          "nonOptionalKeyInsightHint": false,
          "optional": true,
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
                  "text": "XY"
                },
                {
                  "id": "%s-1-EN",
                  "language": "EN",
                  "title": null,
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            },
            {
              "id": "%s-2",
              "type": "PARAGRAPH",
              "required": null,
              "showHidden": null,
              "order": 2,
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
                  "id": "%s-2-DE",
                  "language": "DE",
                  "title": null,
                  "text": "XY"
                },
                {
                  "id": "%s-2-EN",
                  "language": "EN",
                  "title": null,
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            },
            {
              "id": "%s-3",
              "type": "ANSWER_OPTION",
              "required": true,
              "showHidden": null,
              "order": 3,
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
                  "id": "%s-3-1",
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
                      "id": "%s-3-1-DE",
                      "language": "DE",
                      "title": null,
                      "text": "XY, ,XY",
                      "description": ""
                    },
                    {
                      "id": "%s-3-1-EN",
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
            "type": "VALUE",
            "count": null,
            "nextQuestionId": null,
            "prevQuestionId": null,
            "refQuestionId": null,
            "questionRefLogicId": null,
            "sessionId": null,
            "options": [
              {
                "id": "%s-opt1",
                "order": 1,
                "type": "VALUE_GTE",
                "number": 1,
                "count": null,
                "secondNumber": null,
                "secondCount": null,
                "questionAnswerOptionId": null,
                "secondQuestionAnswerOptionId": null,
                "questionId": "XY",
                "refQuestionId": null
              },
              {
                "id": "%s-opt2",
                "order": 2,
                "type": "VALUE_LT",
                "number": 1,
                "count": null,
                "secondNumber": null,
                "secondCount": null,
                "questionAnswerOptionId": null,
                "secondQuestionAnswerOptionId": null,
                "questionId": "XY",
                "refQuestionId": null
              }
            ],
            "refAdaptions": []
          }
        },''' % (id_base, "true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", id_base, id_base, id_base,id_base, id_base, id_base, id_base, id_base, id_base, id_base, id_base, id_base, id_base),
        "ITEM_LIST_EXPANDABLE": '''
        {
          "id": "%s",
          "type": "ITEM_LIST_EXPANDABLE",
          "number": null,
          "minNumber": null,
          "maxNumber": null,
          "screenDuration": null,
          "reviewAble": true,
          "noAnswerPreselection": null,
          "showHint": null,
          "progress": 5,
          "worldObjectEntryKeyType": null,
          "nonOptionalKeyInsightHint": false,
          "optional": true,
          "firstJourneyQuestion": %s,
          "firstSessionQuestion": %s,
          "questionLoopId": null,
          "translations": [
            {
              "id": "%s-DE",
              "language": "DE",
              "title": "",
              "text": "",
              "notAnsweredText": null
            },
            {
              "id": "%s-EN",
              "language": "EN",
              "title": "",
              "text": "",
              "notAnsweredText": null
            }
          ],
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
                  "text": "XY"
                },
                {
                  "id": "%s-1-EN",
                  "language": "EN",
                  "title": "",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            },
            {
              "id": "%s-2",
              "type": "PARAGRAPH",
              "required": null,
              "showHidden": null,
              "order": 2,
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
                  "id": "%s-2-DE",
                  "language": "DE",
                  "title": null,
                  "text": "XY"
                },
                {
                  "id": "%s-2-EN",
                  "language": "EN",
                  "title": "",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            },
            {
              "id": "%s-3",
              "type": "ANSWER_OPTION",
              "required": true,
              "showHidden": null,
              "order": 3,
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
                  "id": "%s-3-1",
                  "order": 1,
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
                }
              ]
            }
          ],
          "nextLogic": {
            "id": "%s",
            "type": "NEXT",
            "count": null,
            "nextQuestionId": "XY",
            "prevQuestionId": null,
            "refQuestionId": null,
            "questionRefLogicId": null,
            "sessionId": null,
            "options": [],
            "refAdaptions": []
          }
        },''' % (id_base, "true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", id_base, id_base, id_base,id_base, id_base, id_base, id_base, id_base, id_base, id_base, id_base),
        "AUDIO":'''
        {
          "id": "%s",
          "type": "CONTENT",
          "number": null,
          "minNumber": null,
          "maxNumber": null,
          "screenDuration": null,
          "reviewAble": null,
          "noAnswerPreselection": null,
          "showHint": null,
          "progress": 6,
          "worldObjectEntryKeyType": null,
          "nonOptionalKeyInsightHint": false,
          "optional": true,
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
                  "text": "XY"
                },
                {
                  "id": "%s-1-EN",
                  "language": "EN",
                  "title": null,
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            },
            {
              "id": "%s-2",
              "type": "PARAGRAPH",
              "required": null,
              "showHidden": null,
              "order": 2,
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
                  "id": "%s-2-DE",
                  "language": "DE",
                  "title": null,
                  "text": "XY"
                },
                {
                  "id": "%s-2-EN",
                  "language": "EN",
                  "title": null,
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            },
            {
              "id": "%s-3",
              "type": "AUDIO",
              "required": null,
              "showHidden": null,
              "order": 3,
              "imageName": null,
              "audioName": "XY",
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
              "language": "DE",
              "contentShowType": null,
              "worldObjectEntryKey": null,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [],
              "answerOptions": []
            },
            {
              "id": "%s-4",
              "type": "AUDIO",
              "required": null,
              "showHidden": null,
              "order": 3,
              "imageName": null,
              "audioName": "XY",
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
              "language": "EN",
              "contentShowType": null,
              "worldObjectEntryKey": null,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [],
              "answerOptions": []
            },
            {
              "id": "%s-5",
              "type": "MORE_INFORMATION_EXPANDED",
              "required": null,
              "showHidden": null,
              "order": 4,
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
                  "id": "%s-5-DE",
                  "language": "DE",
                  "title": "Text zur Audioreise anzeigen",
                  "text": "XY"
                },
                {
                  "id": "%s-5-EN",
                  "language": "EN",
                  "title": "Show audio journey text",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            }
          ],
          "nextLogic": {
            "id": "%s",
            "type": "NEXT",
            "count": null,
            "nextQuestionId": "XY",
            "prevQuestionId": null,
            "refQuestionId": null,
            "questionRefLogicId": null,
            "sessionId": null,
            "options": [],
            "refAdaptions": []
          }
        },''' % (id_base, "true" if count == 0 and write_beginning == True else "null", "true" if count == 0 and write_beginning == True else "null", id_base, id_base, id_base,id_base, id_base, id_base, id_base, id_base, id_base, id_base, id_base, id_base),
        } 


      # WRITE & remove comma for the last entry
      if count == (len(questions_array)-1):
        file.write(questions_dict[question][:-1])
      else:
        file.write(questions_dict[question])


# ENDING
    if write_ending:   
        file.write('''
      ],
      "questionLoops": []
    }
  ]
}
        '''
        )
printie = ('''JIPIIEE - 
ITS DONE''')
print(printie)