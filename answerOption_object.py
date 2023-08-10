import numpy as np
from helper import get_content_length, increase_order_id, add_quotation_mark
from tests import test_if_button_texts_are_the_same

class AnswerOption():
    def __init__(self, question):
        # Attributes
        self.structure = question.structure
        self.texts = question.texts
        self.texts_en = question.texts_en
        self.question = question
        self.required = question.answer_required
        self.options_order = 1
        self.content_length = get_content_length(self.structure) # 0 & answeroption
        self.order = self.content_length
        self.id = question.id + '-' + str(self.content_length)
        self.options_id = question.id + '-' + str(self.content_length) + '-' +str(self.options_order)
        # Preparations
        self.button_texts, self.button_texts_en = self.prepare_button()
        # Options
        self.options = self.create_options()
        # Json
        self.json = self.create_json()

  # ------ PREPARATIONS -----------

    def prepare_button(self):
       # button logics
        if 'BUTTON' in self.structure:
            # Test -> for buttons
            self.button_texts = self.texts[np.where(self.structure == 'BUTTON')]
            for button_text in self.button_texts:
                if not '->' in button_text:
                    raise Exception ('"->" missing at one of the Buttons')
            for i, button in enumerate(self.button_texts):
              self.button_texts[i] = button.split('->')[0].strip()

            # Englisch
            if self.question.english_translation:
              self.button_texts_en = self.texts_en[np.where(self.structure == 'BUTTON')]
              for i, button in enumerate(self.button_texts_en):
                self.button_texts_en[i] = button.split('->')[0].strip()
            else:
               self.button_texts_en = []
               for i in range(len(self.button_texts)):
                  self.button_texts_en.append('Englisch')
            
            # TEST
            test_if_button_texts_are_the_same(self.question.excel_id, self.button_texts)
        else:
           self.button_texts = None
           self.button_texts_en = None

        return self.button_texts, self.button_texts_en
        

  # ------- OPTIONS ---------

    def create_options(self):
      self.options = []
      for struc in self.structure:
        if (self.question.type == 'ITEM_LIST_SINGLE_CHOICE' or self.question.type == 'ITEM_LIST_SINGLE_CHOICE_INTERRUPTIBLE_START') and struc == 'ITEM(Single)':
          self.options.append(AnswerOptionOption(self, 'RADIO_BUTTON'))
          self.options_order, self.options_id = increase_order_id(self.options_order, self.options_id)
        elif self.question.type == 'ITEM_LIST_EXPANDABLE' and struc == 'ITEM(Multiple)':
          self.options.append(AnswerOptionOption(self, 'CHECKBOX'))
          self.options_order, self.options_id = increase_order_id(self.options_order, self.options_id)
        elif self.question.type == 'ITEM_LIST_EXPANDABLE' and struc == 'SEVERAL ANSWER OPTIONS' and not ('ITEM(Multiple)' or 'ITEM(Single)') in self.structure:
          self.options.append(AnswerOptionOption(self, 'TEXT_FIELD_EXPANDABLE'))
          self.options_order, self.options_id = increase_order_id(self.options_order, self.options_id)
        elif self.question.type == 'ITEM_LIST_LIMIT' and struc == 'ITEM(Multiple)':
          self.options.append(AnswerOptionOption(self, 'CHECKBOX'))
          self.options_order, self.options_id = increase_order_id(self.options_order, self.options_id)

      if self.question.type == 'OPTION_QUESTION':
          i = 0
          for struc in self.structure:
             if struc == 'BUTTON':
              self.options.append(AnswerOptionOption(self, 'BUTTON', i))
              self.options_order, self.options_id = increase_order_id(self.options_order, self.options_id)
              i += 1
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
      self.description = 'null'
      self.description_en = 'null'

      # Preparations
      needs_translation = ['RADIO_BUTTON', 'CHECKBOX', 'BUTTON', 'SLIDER']
      if self.type == 'BUTTON':
        self.text = self.answerOption.button_texts[button_number].strip()
        self.text_en = self.answerOption.button_texts_en[button_number]
      if self.type == 'SLIDER':
        self.text = self.answerOption.question.scala_min_text+', ,'+self.answerOption.question.scala_max_text
        self.text_en = self.answerOption.question.scala_min_text_en+', ,'+self.answerOption.question.scala_max_text_en
      if self.type == 'RADIO_BUTTON':
        self.text = answerOption.question.texts[np.where((answerOption.question.structure == 'ITEM(Single)') | (answerOption.question.structure == 'ITEM(Multiple)'))[0][0]+self.order-1].strip()
        if '->' in self.text:
          self.text = self.text.split('->')[0].strip()
        if self.answerOption.question.english_translation:
          self.text_en = answerOption.question.texts_en[np.where((answerOption.question.structure == 'ITEM(Single)') | (answerOption.question.structure == 'ITEM(Multiple)'))[0][0]+self.order-1]
          if '->' in self.text_en:
            self.text_en = self.text_en.split('->')[0].strip()
        else:
           self.text_en = 'Englisch'
      if self.type == 'CHECKBOX':
        self.prepare_checkbox()
      

      if self.type in needs_translation:
        self.translations = '''
                            {
                          "id": "%s-DE",
                          "language": "DE",
                          "title": null,
                          "text": "%s",
                          "description": %s
                        },
                        {
                          "id": "%s-EN",
                          "language": "EN",
                          "title": null,
                          "text": "%s",
                          "description": %s
                        }''' %(self.id, self.text, self.description, self.id, self.text_en, self.description_en)
      else:
        self.translations = ''
        
      # Json
      self.json = self.create_json()

    # -------- PREPARATION -------------
    def prepare_checkbox(self):
      self.text = self.answerOption.question.texts[np.where((self.answerOption.question.structure == 'ITEM(Single)') | (self.answerOption.question.structure == 'ITEM(Multiple)'))[0][0]+self.order-1]
      self.text, self.description = self.check_for_added_information(self.text, self.description)
      if '->' in self.text:
         self.text = self.text.split('->')[0].strip()
      if self.answerOption.question.english_translation:
        self.text_en = self.answerOption.question.texts_en[np.where((self.answerOption.question.structure == 'ITEM(Single)') | (self.answerOption.question.structure == 'ITEM(Multiple)'))[0][0]+self.order-1]
        self.text_en, self.description_en = self.check_for_added_information(self.text_en, self.description_en)
        if '->' in self.text_en:
          self.text_en = self.text_en.split('->')[0].strip()
      else:
          self.text_en = 'Englisch'
      if self.description != 'null' and not self.answerOption.question.english_translation:
        self.description_en = add_quotation_mark('Englisch')
      self.text = self.text.strip()

    def check_for_added_information(self, text, description):
       # check for added information with i= or i =
        if 'i =' in text:
           description = add_quotation_mark(text.split('i =')[1].strip())
           text = text.split('i =')[0].strip()
        elif 'i=' in text:
           description = add_quotation_mark(text.split('i=')[1].strip())
           text = text.split('i=')[0].strip()
        
        return text, description
       

    # ------- JSON ----------

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
            