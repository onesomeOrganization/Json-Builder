from helper import normal_screen_reference, get_one_id_higher

class Content:
  def __init__(self, id, structure, texts):
    self.structure = structure
    self.texts = texts
    self.order = 2
    self.id = id + '-' +str(self.order)
    self.json = ''
    self.create_json()

  def create_json(self):
    for text_count, entry in enumerate(self.structure):
      if entry == 'REFERENCE':
        self.json += self.create_ref(text_count)
        self.order+=1
        self.id = '-'.join(self.id.split('-')[:-1] + [str(self.order)])
      elif entry == 'PARAGRAPH':
        self.json += self.create_par(text_count)
        self.order+=1
        self.id = '-'.join(self.id.split('-')[:-1] + [str(self.order)])
      elif entry == 'AUDIO':
        self.json += self.create_audio(text_count)
        self.order+=2
        self.id = '-'.join(self.id.split('-')[:-1] + [str(self.order)])
      elif entry == 'IMAGE':
        self.json += self.create_image(text_count)
        self.order+=2
        self.id = '-'.join(self.id.split('-')[:-1] + [str(self.order)])
      elif entry == 'MORE_INFORMATION_EXPANDED':
        self.json += self.create_more_information_expanded(text_count)
        self.order+=1
        self.id = '-'.join(self.id.split('-')[:-1] + [str(self.order)])
      elif entry == 'MORE_INFORMATION':
        self.json += self.create_more_information(text_count)
        self.order+=1
        self.id = '-'.join(self.id.split('-')[:-1] + [str(self.order)])

  def create_ref(self, text_count):
    if normal_screen_reference(self.texts[text_count]):
      # create referenz-id
      id_splits = self.id.split('-')
      ref_numbers = self.texts[text_count].split('.')
      refQuestionId = id_splits[0]+'-'+id_splits[1]+'-'+ref_numbers[0]+'-'+ref_numbers[1]

      referenzierung = '''  
              ,{
                "id": "%s",
                "type": "ANSWER_OPTION_REF",
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
                "refQuestionId": "%s",
                "refQuestionAnswerOptionId": null,
                "translations": [],
                "answerOptions": []
              }'''%(self.id, self.order, refQuestionId)
    else: # can be keyinsight or reference out of reflogic 
      worldObjectEntryKey = self.texts[text_count] if self.texts[text_count] == 'null' else '"'+self.texts[text_count]+'"'     
      referenzierung = '''  
            ,{
              "id": "%s",
              "type": "ANSWER_OPTION_REF",
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
              "worldObjectEntryKey": %s,
              "refQuestionId": null,
              "refQuestionAnswerOptionId": null,
              "translations": [],
              "answerOptions": []
            }'''%(self.id, self.order, worldObjectEntryKey)
    return referenzierung

  def create_more_information(self, text_count):
    splitted_text = self.texts[text_count].split('_')
    title = splitted_text[1]
    text = splitted_text[2]
    more_information = '''
            ,{
              "id": "%s",
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
                  "id": "%s-DE",
                  "language": "DE",
                  "title": "%s",
                  "text": "%s"
                },
                {
                  "id": "%s-EN",
                  "language": "EN",
                  "title": "Englisch",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            }'''%(self.id, self.order, self.id, title, text, self.id)
    return more_information

  def create_par(self, text_count):
    paragraph = '''
            ,{
              "id": "%s",
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
                  "id": "%s-DE",
                  "language": "DE",
                  "title": null,
                  "text": "%s"
                },
                {
                  "id": "%s-EN",
                  "language": "EN",
                  "title": null,
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            }'''%(self.id, self.order, self.id, self.texts[text_count], self.id)
    return paragraph

  def create_audio(self, text_count):
    second_id = get_one_id_higher(self.id)
    audioName = self.texts[text_count]
    audio = '''
            ,{
              "id": "%s",
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
              "id": "%s",
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
            }'''%(self.id, self.order, audioName, second_id, self.order+1, audioName)
    return audio

  def create_image(self, text_count):
    imageName = self.texts[text_count]
    second_id = get_one_id_higher(self.id)
    image = '''
            ,{
              "id": "%s",
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
              "id": "%s",
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
            }'''%(self.id, self.order, imageName, second_id, self.order+1, imageName)
    return image

  def create_more_information_expanded(self, text_count):
    splitted_text = self.texts[text_count].split('_')
    title = splitted_text[1]
    text = splitted_text[2]
    more_information_expanded = '''
            ,{
              "id": "%s",
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
                  "id": "%s-DE",
                  "language": "DE",
                  "title": "%s",
                  "text": "%s"
                },
                {
                  "id": "%s-EN",
                  "language": "EN",
                  "title": "Englisch",
                  "text": "Englisch"
                }
              ],
              "answerOptions": []
            }'''%(self.id, self.order, self.id, title, text, self.id)
    return more_information_expanded



