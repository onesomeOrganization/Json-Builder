
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
            }'''%(id_base, count, count, id_base, count+1, count+1)
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
            }'''%(id_base, count, count, id_base, count+1, count+1)
  return image

def create_more_information(id_base, count):
  more_information = '''
            ,{
              "id": "%s-%s",
              "type": "MORE_INFORMATION_EXPANDED",
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
                  "title": "Text zur Audioreise anzeigen",
                  "text": "XY"
                },
                {
                  "id": "%s-%s-EN",
                  "language": "EN",
                  "title": "Englisch",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            }'''%(id_base, count, count, id_base, count, id_base, count)
  return more_information

def create_content_block(id_base, count, refs):
  ref_block = '' 
  for letter in refs:
    if letter == 'R':
      ref_block += create_ref(id_base, count)
      count+=1
    elif letter == 'P':
      ref_block += create_par(id_base, count)
      count+=1
    elif letter == 'A':
      ref_block += create_audio(id_base, count)
      count+=2
    elif letter == 'I':
      ref_block += create_image(id_base, count)
      count+=2
    elif letter == 'M':
      ref_block += create_more_information(id_base, count)
      count+=1

  return ref_block

