import numpy as np
from helper import get_content_length, increase_order_id

class AnswerOption():
    def __init__(self, question):
        # Attributes
        self.structure = question.structure
        self.texts = question.texts
        self.question = question
        self.order = 1
        self.content_length = get_content_length(self.structure) +2 # 0 & answeroption
        self.id = question.id + '-' + str(self.content_length) + '-' +str(self.order)
        # Options
        self.options = self.create_options()
        # Json
        self.json = self.create_json()

  # ------- OPTIONS ---------

    def create_options(self):
      self.options = []
      for struc in self.structure:
        if self.question.type == 'ITEM_LIST_SINGLE_CHOICE' and struc == 'ITEM(Single)':
          self.options.append(AnswerOptionOption(self, 'RADIO_BUTTON'))
          self.order, self.id = increase_order_id(self.order, self.id)
        elif self.question.type == 'ITEM_LIST_EXPANDABLE' and struc == 'ITEM(Multiple)':
          self.options.append(AnswerOptionOption(self, 'CHECKBOX'))
          self.order, self.id = increase_order_id(self.order, self.id)
        elif self.question.type == 'ITEM_LIST_EXPANDABLE' and struc == 'SEVERAL ANSWER OPTIONS' and not ('ITEM(Multiple)' or 'ITEM(Single)') in self.structure:
          self.options.append(AnswerOptionOption(self, 'TEXT_FIELD_EXPANDABLE'))
          self.order, self.id = increase_order_id(self.order, self.id)
      return self.options
      
  # -------- JSON -------------    

    def create_json(self):
        json = ''
        for option in self.options:
           json += option.json
        json = json[:-1]
        return json
    
class AnswerOptionOption():
    def __init__(self, answerOption, type) -> None:
      self.answerOption = answerOption
      self.type = type
      self.order = answerOption.order
      self.id = answerOption.id
      if self.type == 'RADIO_BUTTON' or self.type == 'CHECKBOX':
        self.text = answerOption.question.texts[np.where((answerOption.question.structure == 'ITEM(Single)') | (answerOption.question.structure == 'ITEM(Multiple)'))[0][0]+answerOption.order-1]
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
            