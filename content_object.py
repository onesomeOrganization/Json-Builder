from helper import normal_screen_reference, increase_order_id, create_id, content_length_dict, add_quotation_mark
from tests import test_if_ref_question_is_optional, test_if_question_has_something_to_reference

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
          self.order, self.id = increase_order_id(self.order, self.id, content_length_dict[entry])
        elif entry == 'SUB_TITLE':
          self.contents.append(ContentComponent(self, 'SUB_TITLE', text_count))
          self.order, self.id = increase_order_id(self.order, self.id, content_length_dict[entry])
        elif entry == 'PARAGRAPH':
          self.contents.append(ContentComponent(self, 'PARAGRAPH', text_count))
          self.order, self.id = increase_order_id(self.order, self.id, content_length_dict[entry])
        elif entry == 'AUDIO':
          self.contents.append(ContentComponent(self, 'AUDIO', text_count))
          self.order, self.id = increase_order_id(self.order, self.id, content_length_dict[entry])
        elif entry == 'IMAGE':
          self.contents.append(ContentComponent(self, 'IMAGE', text_count))
          self.order, self.id = increase_order_id(self.order, self.id, content_length_dict[entry])
        elif entry == 'SMALL_IMAGE':
          self.contents.append(ContentComponent(self, 'SMALL_IMAGE', text_count))
          self.order, self.id = increase_order_id(self.order, self.id, content_length_dict[entry])
        elif entry == 'MORE_INFORMATION_EXPANDED':
          self.contents.append(ContentComponent(self, 'MORE_INFORMATION_EXPANDED', text_count))
          self.order, self.id = increase_order_id(self.order, self.id, content_length_dict[entry])
        elif entry == 'MORE_INFORMATION':
          self.contents.append(ContentComponent(self, 'MORE_INFORMATION', text_count))
          self.order, self.id = increase_order_id(self.order, self.id, content_length_dict[entry])
        elif entry == 'PDF_DOWNLOAD':
          self.contents.append(ContentComponent(self, 'PDF_DOWNLOAD', text_count))
          self.order, self.id = increase_order_id(self.order, self.id, content_length_dict[entry])
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
      self.content = Content
      self.worldObjectEntryKey = 'null'
      self.refQuestionId = 'null'
      self.imageName = 'null'
      self.audioName = 'null'
      self.imageName_en = 'null'
      self.audioName_en = 'null'
      self.downloadName = 'null'
      self.downloadName_en = 'null'
      self.translations = ''
      self.title = 'null'
      self.title_en = 'null'
      self.language = 'null'
      if self.type == 'ANSWER_OPTION_REF':
        self.style = Content.question.reference_style
      else:
        self.style = 'null'
      
      needs_translations = ['MORE_INFORMATION', 'MORE_INFORMATION_EXPANDED', 'PARAGRAPH', 'SUB_TITLE']
      self.needs_english_copy = ['AUDIO', 'IMAGE', 'SMALL_IMAGE', 'PDF_DOWNLOAD']

      # Preparations
      if self.type == 'ANSWER_OPTION_REF':
        if normal_screen_reference(self.text):
          self.refQuestionId = '"'+create_id(Content.question, self.text)+'"'
          test_if_ref_question_is_optional(self)
          test_if_question_has_something_to_reference(self)
          for q in self.content.question.questions_before:
            if q.excel_id == self.text:
              if q.type == 'SCALA_SLIDER':
                self.style = add_quotation_mark('SCALA')
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

      if self.type == 'PDF_DOWNLOAD':
        self.downloadName = '"'+self.text+'"'
        self.language = '"'+'DE'+'"'
        if Content.question.english_translation:
          self.downloadName_en = '"'+self.text_en+'"'
        else:
          self.downloadName_en = self.downloadName

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
              "style": %s,
              "refAdaptionType": null,
              "refAdaptionNumber": null,
              "refOrderType": null,
              "refOrderColumn": null,
              "refOffset": null,
              "refLimit": null,
              "downloadName": %s,
              "checkForSpecialTextReplacement": null,
              "questionAnswerOptionId": null,
              "language": %s,
              "contentShowType": null,
              "worldObjectEntryKey": %s,
              "refQuestionId": %s,
              "refQuestionAnswerOptionId": null,
              "translations": [%s],
              "answerOptions": []
            },'''%(self.id, self.type, self.order, self.imageName, self.audioName, self.style, self.downloadName, self.language, self.worldObjectEntryKey, self.refQuestionId, self.translations)
      
      if self.type in self.needs_english_copy:
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
    
