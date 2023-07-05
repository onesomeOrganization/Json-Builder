from helper import normal_screen_reference, increase_order_id, create_id

class Content:
  def __init__(self, question):
    # Attributes
    self.question = question
    self.structure = question.structure
    self.texts = question.texts
    self.texts_en = question.texts_en
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
          self.contents.append(ContentComponent(self, 'ANSWER_OPTION_REF', text_count))
          self.order, self.id = increase_order_id(self.order, self.id)
        elif entry == 'SUB_TITEL':
          self.contents.append(ContentComponent(self, 'SUB_TITEL', text_count))
          self.order, self.id = increase_order_id(self.order, self.id)
        elif entry == 'PARAGRAPH':
          self.contents.append(ContentComponent(self, 'PARAGRAPH', text_count))
          self.order, self.id = increase_order_id(self.order, self.id)
        elif entry == 'AUDIO':
          self.contents.append(ContentComponent(self, 'AUDIO', text_count))
          self.order, self.id = increase_order_id(self.order, self.id, 2)
        elif entry == 'IMAGE':
          self.contents.append(ContentComponent(self, 'IMAGE', text_count))
          self.order, self.id = increase_order_id(self.order, self.id, 2)
        elif entry == 'SMALL_IMAGE':
          self.contents.append(ContentComponent(self, 'SMALL_IMAGE', text_count))
          self.order, self.id = increase_order_id(self.order, self.id, 2)
        elif entry == 'MORE_INFORMATION_EXPANDED':
          self.contents.append(ContentComponent(self, 'MORE_INFORMATION_EXPANDED', text_count))
          self.order, self.id = increase_order_id(self.order, self.id)
        elif entry == 'MORE_INFORMATION':
          self.contents.append(ContentComponent(self, 'MORE_INFORMATION', text_count))
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
    def __init__(self, Content, type, text_count) -> None:
      # Attributes
      self.type = type
      self.text = Content.texts[text_count]
      if Content.question.english_translation:
        self.text_en = Content.texts_en[text_count]
      else:
        self.text_en = 'Englisch'
      self.id = Content.id
      self.order = Content.order
      self.worldObjectEntryKey = 'null'
      self.refQuestionId = 'null'
      self.imageName = 'null'
      self.audioName = 'null'
      self.imageName_en = 'null'
      self.audioName_en = 'null'
      self.translations = ''
      self.title = 'null'
      self.title_en = 'null'
      self.language = 'null'
      

      # Preparations
      if self.type == 'ANSWER_OPTION_REF':
        if normal_screen_reference(self.text):
          self.refQuestionId = '"'+create_id(Content.question, self.text)+'"'
        else:
          self.worldObjectEntryKey = self.text if self.text == 'null' else '"'+self.text +'"'  
      
      if self.type == 'MORE_INFORMATION' or self.type == 'MORE_INFORMATION_EXPANDED':
        splitted_text = self.text.split('_')
        self.title = '"'+splitted_text[1]+'"'
        self.text = splitted_text[2]
        if Content.question.english_translation:
          splitted_text_en = self.text_en.split('_')
          self.title_en = '"'+splitted_text_en[1]+'"'
          self.text_en = splitted_text_en[2]
        else:
          self.title_en = '"Englisch"'

      if self.type == 'IMAGE' or self.type == 'SMALL_IMAGE':
        self.imageName = '"'+self.text+'"'
        self.language = '"'+'DE'+'"'
        if Content.question.english_translation:
          self.imageName_en = '"'+self.text_en+'"'
        else:
          self.imageName_en = self.imageName

      if self.type == 'AUDIO':
        self.audioName = '"'+self.text+'"'
        self.language = '"'+'DE'+'"'
        if Content.question.english_translation:
          self.audioName_en = '"'+self.text_en+'"'
        else:
          self.audioName_en = self.audioName

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
                  "title": %s,
                  "text": "%s"
                }'''%(self.id, self.title, self.text, self.id, self.title_en, self.text_en)

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
              "language": %s,
              "contentShowType": null,
              "worldObjectEntryKey": %s,
              "refQuestionId": %s,
              "refQuestionAnswerOptionId": null,
              "translations": [%s],
              "answerOptions": []
            },'''%(self.id, self.type, self.order, self.imageName, self.audioName, self.language, self.worldObjectEntryKey, self.refQuestionId, self.translations)
      
      if self.type == 'AUDIO' or self.type == 'IMAGE' or self.type == 'SMALL_IMAGE':
          self.order, self.id = increase_order_id(self.order,self.id)
          self.language = '"'+'EN'+'"'
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
              "language": %s,
              "contentShowType": null,
              "worldObjectEntryKey": %s,
              "refQuestionId": %s,
              "refQuestionAnswerOptionId": null,
              "translations": [%s],
              "answerOptions": []
            },'''%(self.id, self.type, self.order, self.imageName_en, self.audioName_en, self.language, self.worldObjectEntryKey, self.refQuestionId, self.translations)
      return json
    
