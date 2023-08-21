from question_object import Question
from tests import are_all_information_there, test_aufruf, do_tests_for_question_array
from progress import create_progress, create_adjazenzliste
import pandas as pd
import re
from questionLoops_object import create_questionloops

class Trip:
    def __init__(self, df, id_base, version, write_beginning, write_ending, journey_key, english_translation, etappe, starts_in_the_middle_of_etappe, nummeration_is_not_correct):
        # Attributes
        self.df = df
        self.id = id_base+version
        self.id_base = id_base
        self.key = journey_key
        self.etappe = etappe
        self.nummeration_is_not_correct = nummeration_is_not_correct
        self.starts_in_the_middle_of_etappe = starts_in_the_middle_of_etappe
        self.english_translation = english_translation
        self.information, self.information_en = self.create_information()
        self.mainImageName = self.information[9]
        self.mainImageLongName = self.information[10]
        self.topicIconImageName = self.information[11]
        self.mainImageLockedLongName = self.information[12]
        self.backgroundImageName = self.information[13]
        self.sessionImageName = self.information[14]
        self.cardDisplayImageName = self.information[15]
        self.version = version[1:]
        self.type = self.information[0]
        self.topicId = self.information[1]
        self.title = self.information[2]
        self.beschreibung = self.information[3].replace('"', '\\"').replace('\n', '').replace("_x000B_", "")+'<br><br>'
        self.aufruf = self.information[4]
        self.etappen_titel = self.information[5]
        self.durationMin = self.information[7]
        self.durationMax = self.information[8]
        self.write_beginning = write_beginning
        self.write_ending = write_ending

        if english_translation:
            self.title_en = self.information_en[2]
            self.beschreibung_en = self.information_en[3].replace('"', '\\"').replace('\n', '').replace("_x000B_", "")+'<br><br>'
            self.aufruf_en = self.information_en[4]
            self.etappen_titel_en = self.information_en[5]
        else:
            self.title_en = 'Englisch'
            self.beschreibung_en = 'Englisch'
            self.aufruf_en = 'Englisch'
            self.etappen_titel_en = 'Englisch'

        # Preparations
        self.all_ids = self.get_all_ids()
        self.all_questions_array = self.create_questions_array()
        self.etappen_count = self.get_etappen_count()
        self.etappen_end_screens = self.calc_etappen_end_screens()
        self.etappen_start_screens = self.get_etappen_start_screens()
        do_tests_for_question_array(self)
        self.graph = create_adjazenzliste(self.all_questions_array)
        self.qloop_start_screens_ids = self.get_qloop_start_screens()
        loop_dict = create_progress(self, self.all_questions_array)
        self.questionLoops = create_questionloops(self, loop_dict)
        # Json
        self.json = self.create_json()

    # ------ PREPARATIONS -----------

    def get_qloop_start_screens(self):
        qloop_start_screens_ids = []
        for q in self.all_questions_array:
            if q.qloop_start:
                qloop_start_screens_ids.append(q.excel_id)
        return qloop_start_screens_ids
        

    def create_information(self):
        # get first informations and set defaults
      information = self.df.iloc[:, 1]
      information_en = self.df.iloc[:,2]

      are_all_information_there(information, information_en, self.english_translation)

      if information[0] == 'Reise' or information[0] == 'reise':
          information[0] = 'WORLD'
          information[1] = '"'+information[1]+'"'
          information[15] = '"'+information[15]+'"'
          
      if information[0] == 'Kurztrip' or information[0] == 'kurztrip':
          information[0] = 'SHORT_TRIP'
          information[1] = 'null'
          information[15] = 'null'

      test_aufruf(information, information_en, self.english_translation)
      return information, information_en


    def create_questions_array(self):
        questions_array = []
        for i in range(3, len(self.df.columns), 3): # start at 3 because of the information
            # Create a boolean mask to check if values are None
            mask = self.df.iloc[:, i] == 'None'
            # Check if all values in the column are None
            if mask.all():
                if self.df.columns[i] != None:
                    raise Exception ('Structures missing at question: ', self.df.columns[i])
                break
            if (i+4) > (len(self.df.columns)-1):
                next_question_structure = []
                next_question_texts = []
            else:
                next_question_structure = self.df.iloc[:, i+3]
                next_question_texts = self.df.iloc[:, i+4]
            questions_array.append(Question(self, self.id_base, self.version, self.df.iloc[:, i], self.df.iloc[:, i+1], self.df.iloc[:, i+2], next_question_structure, next_question_texts, self.df.columns[i], self.write_beginning, self.write_ending, self.english_translation, questions_array))
        return questions_array         

    def format_text(self):
      for question in self.all_questions_array:
          for i, text in enumerate(question.texts):
              if not pd.isnull(text):
              # find " and replace with \"
              # find breaks and delete them
                  question.texts[i] = text.replace('"', '\\"').replace('\n', '').replace("_x000B_", "")

          if self.english_translation:
              for i, text in enumerate(question.texts_en):
                if not pd.isnull(text):
              # find " and replace with \"
              # find breaks and delete them
                  question.texts_en[i] = text.replace('"', '\\"').replace('\n', '').replace("_x000B_", "")

    def get_all_ids(self):
        ids = []
        pattern = '^\d+\.\d+(x?)$'
        for id in self.df.columns:
            if id is not None and re.match(pattern, id):
              ids.append(id)
            if id is not None and not re.match(pattern, id) and id != 'Informationen' and id != 'Informationen Text':
                raise Exception ('Id is not correct at question: ', id, ' (ids with x have to look like e.g 3.5x not 3.x)')
        return ids
    
    def get_etappen_count(self):
        etappen_count = set()
        for q in self.all_questions_array:
            etappen_count.add(q.excel_id[0])
        return len(etappen_count)

    def calc_etappen_end_screens(self):
        # which screens are the last screen in an etappe
        etappen_end_screens = {}
        for etappe in range(1, self.etappen_count+1):
            etappe = self.etappe+etappe-1
            for num, question in enumerate(self.all_questions_array):
                if int(question.excel_id[0]) == etappe:
                    # letzter screen is alsways end screen
                    if 'letzter Screen' in question.structure:
                        if question.excel_id[0] in etappen_end_screens:
                            array = etappen_end_screens[question.excel_id[0]]
                            array.append(question.excel_id)
                        else:
                          etappen_end_screens[question.excel_id[0]] = [question.excel_id]
                    # letzte Frage im Array
                    elif num+1 == len(self.all_questions_array) and not 'weiter mit Screen' in question.structure:
                            if question.excel_id[0] in etappen_end_screens:
                              array = etappen_end_screens[question.excel_id[0]]
                              array.append(question.excel_id)
                            else:
                              etappen_end_screens[question.excel_id[0]] = [question.excel_id]
                    # letzter Screen vergessen
                    elif num+1 == len(self.all_questions_array):
                      if len(etappen_end_screens)==0:
                        raise Exception ('"letzter Screen" is missing somewhere in the Excel')
                      else:
                          return etappen_end_screens
                    # Ende von Etappe
                    elif 'Neue Etappe' in self.all_questions_array[num+1].structure and not 'weiter mit Screen' in question.structure:
                        if question.excel_id[0] in etappen_end_screens:
                              array = etappen_end_screens[question.excel_id[0]]
                              array.append(question.excel_id)
                        else:
                              etappen_end_screens[question.excel_id[0]] = [question.excel_id]
        return etappen_end_screens
    
    def get_etappen_start_screens(self):
        etappen_start_screens = []
        if self.starts_in_the_middle_of_etappe:
            etappen_start_screens.append(self.all_ids[0])
            return etappen_start_screens
        for id in self.all_ids:
            if id.split('.')[1] == '1':
                etappen_start_screens.append(id)
        return etappen_start_screens
            

  # -------- JSON ---------------

    def create_beginning(self):
        beginning = '''
    {
      "id": "%s",
      "key": "%s",
      "order": 500,
      "mainImageName": "%s",
      "mainImageLongName": "%s",
      "topicIconImageName": "%s",
      "mainImageLockedLongName": "%s",
      "backgroundImageName": "%s",
      "sessionImageName": "%s",
      "cardDisplayImageName": %s,
      "published": true,
      "publishedEN": false,
      "feedbackLink": null,
      "version": %s,
      "type": "%s",
      "compulsoryOrder": false,
      "topicId": %s,
      "backgroundImageLockedName": "dark_main.png",
      "translations": [
        {
          "id": "%s-DE",
          "language": "DE",
          "title": "%s",
          "subTitle": "",
          "description": null
        },
        {
          "id": "%s-EN",
          "language": "EN",
          "title": "%s",
          "subTitle": "",
          "description": null
        }
      ],
      "content": [
        {
          "id": "%s-cont",
          "order": 2,
          "type": "PARAGRAPH",
          "imageName": null,
          "translations": [
            {
              "id": "%s-cont-DE",
              "language": "DE",
              "title": null,
              "text": "%s"
            },
            {
              "id": "%s-cont-EN",
              "language": "EN",
              "title": null,
              "text": "%s"
            }
          ]
        },
        {
          "id": "%s-s1",
          "order": 4,
          "type": "SESSION_TITLE",
          "imageName": null,
          "translations": [
            {
              "id": "%s-s1-DE",
              "language": "DE",
              "title": null,
              "text": "%s"
            },
            {
              "id": "%s-s1-EN",
              "language": "EN",
              "title": null,
              "text": "%s"
            }
          ]
        }
      ],
      "sessions": [
        {
          "id": "%s-%s",
          "order": %s,
          "durationMin": %s,
          "durationMax": %s,
          "translations": [
            {
              "id": "%s-%s-DE",
              "language": "DE",
              "title": "%s"
            },
            {
              "id": "%s-%s-EN",
              "language": "EN",
              "title": "%s"
            }
          ],
          "questions": [
            ''' % (self.id, self.key, self.mainImageName, self.mainImageLongName, self.topicIconImageName, self.mainImageLockedLongName, self.backgroundImageName, self.sessionImageName, self.cardDisplayImageName, self.version, self.type, self.topicId, self.id, self.title, self.id, self.title_en, self.id, self.id, self.beschreibung, self.id, self.beschreibung_en, self.id, self.id, self.aufruf, self.id, self.aufruf_en, self.id, self.etappe, self.etappe, self.durationMin, self.durationMax, self.id, self.etappe, self.etappen_titel, self.id, self.etappe, self.etappen_titel_en)
        return beginning
    
    def create_json(self):
          json = ''
          # Beginning
          if self.write_beginning:    
              json += self.create_beginning()

          # Questions
          for question in self.all_questions_array: 
              json += question.create_json()

          # Ending
          if self.write_ending:   
           json += '''
      ],
      "questionLoops": [
      %s
      ]
    }
  ]
}
        '''%(self.questionLoops)
          return json



    
        

    