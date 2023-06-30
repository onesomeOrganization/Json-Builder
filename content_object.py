from helper import normal_screen_reference, increase_order_id, create_id

class Content:
  def __init__(self, question):
    # Attributes
    self.question = question
    self.structure = question.structure
    self.texts = question.texts
    self.order = 1
    self.id = question.id + '-' +str(self.order)
    # Contents
    self.contents = self.create_contents()
    # Json
    self.json = self.create_json()
   
  def create_contents(self):
    self.contents = []
    for text_count,entry in enumerate(self.structure):
        if entry == 'REFERENCE':
          self.contents.append(ContentComponent(self, 'ANSWER_OPTION_REF', self.texts[text_count]))
          self.order, self.id = increase_order_id(self.order, self.id)
        elif entry == 'SUB_TITEL':
          self.contents.append(ContentComponent(self, 'SUB_TITEL', self.texts[text_count]))
          self.order, self.id = increase_order_id(self.order, self.id)
        elif entry == 'PARAGRAPH':
          self.contents.append(ContentComponent(self, 'PARAGRAPH', self.texts[text_count]))
          self.order, self.id = increase_order_id(self.order, self.id)
        elif entry == 'AUDIO':
          self.contents.append(ContentComponent(self, 'AUDIO', self.texts[text_count]))
          self.order, self.id = increase_order_id(self.order, self.id, 2)
        elif entry == 'IMAGE':
          self.contents.append(ContentComponent(self, 'IMAGE', self.texts[text_count]))
          self.order, self.id = increase_order_id(self.order, self.id, 2)
        elif entry == 'MORE_INFORMATION_EXPANDED':
          self.contents.append(ContentComponent(self, 'MORE_INFORMATION_EXPANDED', self.texts[text_count]))
          self.order, self.id = increase_order_id(self.order, self.id)
        elif entry == 'MORE_INFORMATION':
          self.contents.append(ContentComponent(self, 'MORE_INFORMATION', self.texts[text_count]))
          self.order, self.id = increase_order_id(self.order, self.id)
    return self.contents

  def create_json(self):
    json = ''
    for content in self.contents:
      json += content.json
    if self.question.type == 'CONTENT':
      json = json[:-1]
    return json


class ContentComponent():
    def __init__(self, Content, type, text) -> None:
      # Attributes
      self.type = type
      self.text = text
      self.id = Content.id
      self.order = Content.order
      self.worldObjectEntryKey = 'null'
      self.refQuestionId = 'null'
      self.imageName = 'null'
      self.audioName = 'null'
      self.translations = ''
      self.title = 'null'

      # Preparations
      if self.type == 'ANSWER_OPTION_REF':
        if normal_screen_reference(text):
          self.refQuestionId = '"'+create_id(Content.question, text)+'"'
        else:
          self.worldObjectEntryKey = self.text if self.text == 'null' else '"'+self.text +'"'  
      
      if self.type == 'MORE_INFORMATION' or self.type == 'MORE_INFORMATION_EXPANDED':
        splitted_text = self.text.split('_')
        self.title = '"'+splitted_text[1]+'"'
        self.text = splitted_text[2]

      if self.type == 'IMAGE':
        self.imageName = '"'+self.text+'"'

      if self.type == 'AUDIO':
        self.audioName = '"'+self.text+'"'

      needs_translations = ['MORE_INFORMATION', 'MORE_INFORMATION_EXPANDED', 'PARAGRAPH', 'SUB_TITEL']
      if self.type in needs_translations:
        self.translations = '''
                {
                  "id": "%s-DE",
                  "language": "DE",
                  "title": %s,
                  "text": "%s"
                },
                {
                  "id": "%s-EN",
                  "language": "EN",
                  "title": "Englisch",
                  "text": "Englisch"
                }'''%(self.id, self.title, self.text, self.id)

      # Json
      self.json = self.create_json()

    def create_json(self):
      json = '''  
            {
              "id": "%s",
              "type": "%s",
              "required": null,
              "showHidden": null,
              "order": %s,
              "imageName": %s,
              "audioName": %s,
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
              "refQuestionId": %s,
              "refQuestionAnswerOptionId": null,
              "translations": [%s],
              "answerOptions": []
            },'''%(self.id, self.type, self.order, self.imageName, self.audioName, self.worldObjectEntryKey, self.refQuestionId, self.translations)
      
      if self.type == 'AUDIO' or self.type == 'IMAGE':
          self.order, self.id = increase_order_id(self.order,self.id)
          json += '''  
            {
              "id": "%s",
              "type": "%s",
              "required": null,
              "showHidden": null,
              "order": %s,
              "imageName": %s,
              "audioName": %s,
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
              "refQuestionId": %s,
              "refQuestionAnswerOptionId": null,
              "translations": [%s],
              "answerOptions": []
            },'''%(self.id, self.type, self.order, self.imageName, self.audioName, self.worldObjectEntryKey, self.refQuestionId, self.translations)
      return json
    
