import re

# ------- HELPER FUNCTIONS ------------------------------

def create_ref(id_base, count, texts, text_count):
  # create referenz-id
  id_splits = id_base.split('-')
  ref_numbers = texts[text_count].split('.')
  reference_id = id_splits[0]+'-'+id_splits[1]+'-'+ref_numbers[0]+'-'+ref_numbers[1]

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
              "refQuestionId": "%s",
              "refQuestionAnswerOptionId": null,
              "translations": [],
              "answerOptions": []
            }'''%(id_base, count, count, reference_id)
  return referenzierung

def create_keyinsight_ref(id_base, count, texts, text_count):
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
              "worldObjectEntryKey": "%s",
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [],
              "answerOptions": []
            }'''%(id_base, count, count, texts[text_count])
  return referenzierung

def create_par(id_base, count, texts, text_count):
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
                  "text": "%s"
                },
                {
                  "id": "%s-%s-EN",
                  "language": "EN",
                  "title": null,
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            }'''%(id_base, count, count, id_base, count,texts[text_count], id_base, count)
  return paragraph

def create_audio(id_base, count, texts, text_count):
  audio = '''
            ,{
              "id": "%s-%s",
              "type": "AUDIO",
              "required": null,
              "showHidden": null,
              "order": %s,
              "imageName": null,
              "audioName": "%s",
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
              "audioName": "%s",
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
            }'''%(id_base, count, count,texts[text_count], id_base, count+1, count+1, texts[text_count])
  return audio

def create_image(id_base, count, texts, text_count):
  image = '''
            ,{
              "id": "%s-%s",
              "type": "IMAGE",
              "required": null,
              "showHidden": null,
              "order": %s,
              "imageName": "%s",
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
              "imageName": "%s",
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
            }'''%(id_base, count, count, texts[text_count], id_base, count+1, count+1, texts[text_count])
  return image

def create_more_information_expanded(id_base, count, texts, text_count):
  splitted_text = texts[text_count].split('_')
  title = splitted_text[1]
  text = splitted_text[2]
  more_information_expanded = '''
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
                  "title": "%s",
                  "text": "%s"
                },
                {
                  "id": "%s-%s-EN",
                  "language": "EN",
                  "title": "Englisch",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            }'''%(id_base, count, count, id_base, count, title, text, id_base, count)
  return more_information_expanded

def create_more_information(id_base, count, texts, text_count):
  splitted_text = texts[text_count].split('_')
  title = splitted_text[1]
  text = splitted_text[2]
  more_information = '''
            ,{
              "id": "%s-%s",
              "type": "MORE_INFORMATION",
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
                  "title": "%s",
                  "text": "%s"
                },
                {
                  "id": "%s-%s-EN",
                  "language": "EN",
                  "title": "Englisch",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            }'''%(id_base, count, count, id_base, count, title, text, id_base, count)
  return more_information

def check_íf_screen_reference(text):
  pattern = '^[+-]?\d+([.,]\d+)?$'
  check = bool(re.match(pattern, text))
  return check

def create_content_block(id_base, count, structure, texts):
  ref_block = '' 
  for i, entry in enumerate(structure):
    if entry == 'REFERENCE' and not check_íf_screen_reference(texts[i]):
      ref_block += create_keyinsight_ref(id_base, count, texts, i)
      count+=1
    elif entry == 'REFERENCE' and check_íf_screen_reference(texts[i]):
      ref_block += create_ref(id_base, count, texts, i)
      count+=1
    elif entry == 'PARAGRAPH':
      ref_block += create_par(id_base, count, texts, i)
      count+=1
    elif entry == 'AUDIO':
      ref_block += create_audio(id_base, count, texts, i)
      count+=2
    elif entry == 'IMAGE':
      ref_block += create_image(id_base, count, texts, i)
      count+=2
    elif entry == 'MORE_INFORMATION_EXPANDED':
      ref_block += create_more_information_expanded(id_base, count, texts, i)
      count+=1
    elif entry == 'MORE_INFORMATION':
      ref_block += create_more_information(id_base, count, texts, i)
      count+=1

  return ref_block 

