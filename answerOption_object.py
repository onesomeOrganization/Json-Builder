import numpy as np
from helper import get_content_length, increase_order_id

class AnswerOption():
    def __init__(self, question):
        # Attributes
        self.structure = question.structure
        self.texts = question.texts
        self.question = question
        self.required = question.answer_required
        self.options_order = 1
        self.content_length = get_content_length(self.structure) +2 # 0 & answeroption
        self.order = self.content_length
        self.id = question.id + '-' + str(self.content_length)
        self.options_id = question.id + '-' + str(self.content_length) + '-' +str(self.options_order)
        # Preparations
        self.button_texts = self.prepare_button()
        # Options
        self.options = self.create_options()
        # Json
        self.json = self.create_json()

  # ------ PREPARATIONS -----------

    def prepare_button(self):
       # button logics
        if 'BUTTON' in self.structure:
            # Test -> for buttons
            button_texts = self.texts[np.where(self.structure == 'BUTTON')]
            for button_text in button_texts:
                if not '->' in button_text:
                    raise Exception ('"->" missing at one of the Buttons')
            button_one = button_texts[0].split('->')
            button_two = button_texts[1].split('->')
            self.button_texts = [button_one[0].strip(), button_two[0].strip()]
        else:
            self.button_texts = []

        return self.button_texts

  # ------- OPTIONS ---------

    def create_options(self):
      self.options = []
      for struc in self.structure:
        if self.question.type == 'ITEM_LIST_SINGLE_CHOICE' and struc == 'ITEM(Single)':
          self.options.append(AnswerOptionOption(self, 'RADIO_BUTTON'))
          self.options_order, self.options_id = increase_order_id(self.options_order, self.options_id)
        elif self.question.type == 'ITEM_LIST_EXPANDABLE' and struc == 'ITEM(Multiple)':
          self.options.append(AnswerOptionOption(self, 'CHECKBOX'))
          self.options_order, self.options_id = increase_order_id(self.options_order, self.options_id)
        elif self.question.type == 'ITEM_LIST_EXPANDABLE' and struc == 'SEVERAL ANSWER OPTIONS' and not ('ITEM(Multiple)' or 'ITEM(Single)') in self.structure:
          self.options.append(AnswerOptionOption(self, 'TEXT_FIELD_EXPANDABLE'))
          self.options_order, self.options_id = increase_order_id(self.options_order, self.options_id)

      if self.question.type == 'OPTION_QUESTION':
          self.options.append(AnswerOptionOption(self, 'BUTTON'))
          self.options_order, self.options_id = increase_order_id(self.options_order, self.options_id)
          self.options.append(AnswerOptionOption(self, 'BUTTON', 1))
          self.options_order, self.options_id = increase_order_id(self.options_order, self.options_id)
      elif self.question.type == 'OPEN_QUESTION':
          self.options.append(AnswerOptionOption(self, 'TEXT_FIELD'))
          self.options_order, self.options_id = increase_order_id(self.options_order, self.options_id)
      elif self.question.type == 'SCALA_SLIDER':
          self.options.append(AnswerOptionOption(self, 'SLIDER'))
          self.options_order, self.options_id = increase_order_id(self.options_order, self.options_id)
      return self.options
      
  # -------- JSON -------------    

    def create_json(self):
        
        if self.question.type == 'CONTENT':
           return ''

        options_json = ''
        for option in self.options:
           options_json += option.json
        options_json = options_json[:-1]

        json = '''
              {
                "id": "%s",
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
                }'''%(self.id, self.required, self.order, options_json)
        return json
    
class AnswerOptionOption():
    def __init__(self, answerOption, type, button_number = 0) -> None:
      # Attributes
      self.answerOption = answerOption
      self.button_number = button_number
      self.type = type
      self.order = answerOption.options_order
      self.id = answerOption.options_id

      # Preparations
      needs_translation = ['RADIO_BUTTON', 'CHECKBOX', 'BUTTON', 'SLIDER']
      if self.type == 'BUTTON':
        self.text = self.answerOption.button_texts[button_number]
      if self.type == 'SLIDER':
         self.text = self.answerOption.question.scala_min_text+', ,'+self.answerOption.question.scala_max_text
      if self.type == 'RADIO_BUTTON' or self.type == 'CHECKBOX':
         self.text = answerOption.question.texts[np.where((answerOption.question.structure == 'ITEM(Single)') | (answerOption.question.structure == 'ITEM(Multiple)'))[0][0]+self.order-1]
      if self.type in needs_translation:
        self.translations = '''
                            {
                          "id": "%s-DE",
                          "language": "DE",
                          "title": null,
                          "text": "%s",
                          "description": ""
                        },
                        {
                          "id": "%s-EN",
                          "language": "EN",
                          "title": null,
                          "text": "Englisch",
                          "description": ""
                        }''' %(self.id, self.text, self.id)
      else:
        self.translations = ''
        
      # Json
      self.json = self.create_json()

    def create_json(self):
       json = '''
                    {
                      "id": "%s",
                      "order": %s,
                      "number": null,
                      "type": "%s",
                      "imageName": null,
                      "hidden": null,
                      "escapeOption": null,
                      "sliderType": null,
                      "negative": null,
                      "unselectOthers": null,
                      "refQuestionAnswerOptionId": null,
                      "questionLoopCycleId": null,
                      "translations": [
                        %s
                      ]
                    },'''%(self.id, self.order, self.type, self.translations)
       return json
            